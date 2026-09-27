import itertools
import typing
from collections import deque
from collections.abc import AsyncGenerator
from datetime import UTC
from datetime import datetime
from typing import Any

from aiogram import Bot
from aiogram.client.session.base import BaseSession
from aiogram.methods import TelegramMethod
from aiogram.methods.base import Request
from aiogram.methods.base import Response
from aiogram.methods.base import TelegramType
from aiogram.types import Chat
from aiogram.types import Message
from aiogram.types import ResponseParameters
from aiogram.types import User
from aiogram.types.base import UNSET_TYPE

from .calls import Calls
from .exceptions import MockedResponseMissingError

DEFAULT_AUTO_MOCK_SUCCESS = True


class MockedSession(BaseSession):
    def __init__(self):
        super().__init__()
        self.responses: deque[Response[TelegramType]] = deque()
        self.requests: deque[Request] = deque()
        self.methods: deque[TelegramMethod] = deque()
        self.closed = True

    def add_result(self, response: Response[TelegramType]) -> Response[TelegramType]:
        self.responses.appendleft(response)
        return response

    def get_request(self) -> Request | None:
        if self.requests:
            return self.requests[-1]

        return None

    async def close(self):
        self.closed = True

    async def make_request(
        self,
        bot: Bot,
        method: TelegramMethod[TelegramType],
        timeout: int | None = UNSET_TYPE,
    ) -> TelegramType:
        self.closed = False
        request = Request(method=method.__api_method__, data=method.__dict__, files=None)
        self.requests.append(request)
        self.methods.append(method)
        if not self.responses and getattr(bot, "auto_mock_success", False):
            # Answer at request time, so a failure queued earlier is never followed by a stale success
            bot.add_result_for(type(method), ok=True, result=bot.default_result(method))
        if not self.responses:
            raise MockedResponseMissingError(
                f"no mocked response for {method.__api_method__}: call "
                f"add_result_for({type(method).__name__}, ...) first or enable auto_mock_success"
            )
        response: Response[TelegramType] = self.responses.pop()
        self.check_response(
            method=method,
            status_code=response.error_code,
            content=response.model_dump_json(),
            bot=bot,
        )
        return response.result  # type: ignore

    async def stream_content(
        self, url: str, timeout: int, chunk_size: int
    ) -> AsyncGenerator[bytes, None]:  # pragma: no cover
        yield b""


class MockedBot(Bot):
    def __init__(self, auto_mock_success: bool = DEFAULT_AUTO_MOCK_SUCCESS, **kwargs):
        super().__init__(kwargs.pop("token", "42:TEST"), session=MockedSession(), **kwargs)
        self._me = User(
            id=self.id,
            is_bot=True,
            first_name="FirstName",
            last_name="LastName",
            username="username",
            language_code="ru",
        )
        self.auto_mock_success = auto_mock_success
        self._message_ids = itertools.count(1)

    def add_result_for(
        self,
        method: type[TelegramMethod[TelegramType]],
        ok: bool,
        result: TelegramType = None,
        description: str | None = None,
        error_code: int = 200,
        migrate_to_chat_id: int | None = None,
        retry_after: int | None = None,
    ) -> Response[TelegramType]:
        response = Response[method.__returning__](  # type: ignore
            ok=ok,
            result=result,
            description=description,
            error_code=error_code,
            parameters=ResponseParameters(
                migrate_to_chat_id=migrate_to_chat_id,
                retry_after=retry_after,
            ),
        )
        self.session.add_result(response)
        return response

    @property
    def calls(self) -> Calls:
        """
        Every Bot API call this bot made, including ones outside the dispatcher (background jobs, notifiers)
        """

        return Calls(self.session.methods)

    def default_result(self, method: TelegramMethod) -> Any:
        """
        What Telegram would plausibly answer to ``method`` when no result was queued: the sent or edited message
        for message methods, ``True`` for boolean ones, the bot itself for ``getMe``
        """

        returning = method.__returning__
        options = typing.get_args(returning) or (returning,)
        if User in options:
            return self._me
        if Message in options and getattr(method, "inline_message_id", None) is None:
            chat_id = getattr(method, "chat_id", None)
            return Message(
                message_id=getattr(method, "message_id", None) or next(self._message_ids),
                date=datetime.now(UTC),
                chat=Chat(id=chat_id if isinstance(chat_id, int) else -1, type="private"),
                from_user=self._me,
                text=getattr(method, "text", None),
                caption=getattr(method, "caption", None),
            )
        if bool in options:
            return True
        if typing.get_origin(returning) is list:
            return []
        return None

    def get_request(self) -> Request:
        return self.session.get_request()
