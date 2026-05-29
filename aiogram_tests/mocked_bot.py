from collections import deque
from collections.abc import AsyncGenerator

from aiogram import Bot
from aiogram.client.session.base import BaseSession
from aiogram.methods import TelegramMethod
from aiogram.methods.base import Request
from aiogram.methods.base import Response
from aiogram.methods.base import TelegramType
from aiogram.types import ResponseParameters
from aiogram.types import User
from aiogram.types.base import UNSET_TYPE

DEFAULT_AUTO_MOCK_SUCCESS = True


class MockedSession(BaseSession):
    def __init__(self):
        super().__init__()
        self.responses: deque[Response[TelegramType]] = deque()
        self.requests: deque[Request] = deque()
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
        self.session = MockedSession()
        self._me = User(
            id=self.id,
            is_bot=True,
            first_name="FirstName",
            last_name="LastName",
            username="username",
            language_code="ru",
        )
        self.auto_mock_success = auto_mock_success

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

    async def __call__(self, method: TelegramMethod, request_timeout: int | None = None):
        if self.auto_mock_success:
            self.add_result_for(method.__class__, ok=True)
        return await super().__call__(method, request_timeout)

    def get_request(self) -> Request:
        return self.session.get_request()
