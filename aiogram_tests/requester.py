import inspect
from collections.abc import Iterator
from typing import Any
from typing import TypeVar

from aiogram.methods import TelegramMethod
from aiogram.methods.base import Response
from aiogram.methods.base import TelegramType

from .exceptions import MethodIsNotCalledError
from .handler.base import RequestHandler
from .utils import camel_case2snake_case

M = TypeVar("M", bound=TelegramMethod)


class CallsList(list[M]):
    def fetchone(self) -> M | None:
        if len(self) > 0:
            return self[-1]
        else:
            return None

    def fetchall(self) -> "CallsList[M]":
        return self


class Calls:
    """
    Bot API methods called while handling one query, in call order.

    ``calls.send_message`` returns the ``SendMessage`` calls; ``calls.get(SendMessage)`` does the same with a type
    the IDE and type checkers understand.
    """

    def __init__(self, methods: list[TelegramMethod] | tuple = ()):
        self._methods = list(methods)
        # Same list on every access: tests pop() from calls.send_message
        self._groups: dict[str, CallsList] = {}
        for m in self._methods:
            self._groups.setdefault(camel_case2snake_case(m.__api_method__), CallsList()).append(m)

    def _get_attributes(self) -> tuple[str, ...]:
        return tuple(self._groups)

    def __getattr__(self, item: str) -> CallsList:
        if item.startswith("_"):
            raise AttributeError(item)
        group = self._groups.get(item)
        if group is None:
            raise MethodIsNotCalledError(
                f"method '{item}' is not called by bot, so you cant to get this attribute. "
                f"Called methods: {self._get_attributes()}"
            )
        return group

    def __iter__(self) -> Iterator[TelegramMethod]:
        return iter(self._methods)

    def __len__(self) -> int:
        return len(self._methods)

    def get(self, method: type[M]) -> CallsList[M]:
        return CallsList(m for m in self._methods if isinstance(m, method))

    def last(self, method: type[M]) -> M | None:
        return self.get(method).fetchone()

    def assert_called(self, method: type[M], **fields: Any) -> M:
        """
        Return the last call of ``method`` whose fields equal ``fields``, fail with the calls that were made otherwise
        """

        candidates = self.get(method)
        for call in reversed(candidates):
            if all(getattr(call, name, None) == value for name, value in fields.items()):
                return call

        expected = ", ".join(f"{name}={value!r}" for name, value in fields.items())
        made = "\n".join(f"  {call!r}" for call in candidates) or f"  none; called methods: {self._get_attributes()}"
        raise AssertionError(f"{method.__name__}({expected}) was not called. {method.__name__} calls:\n{made}")

    def assert_not_called(self, method: type[TelegramMethod]) -> None:
        calls = self.get(method)
        if calls:
            made = "\n".join(f"  {call!r}" for call in calls)
            raise AssertionError(f"{method.__name__} was called {len(calls)} time(s):\n{made}")


class MockedRequester:
    def __init__(self, request_handler: RequestHandler):
        self._handler: RequestHandler = request_handler

    async def query(self, *args, **kwargs) -> Calls:
        self._check_arguments(*args, **kwargs)

        methods = self._handler.bot.session.methods
        already_made = len(methods)
        await self._handler(*args, **kwargs)

        return Calls(list(methods)[already_made:])

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
        response = self._handler.add_result_for(
            method=method,
            ok=ok,
            result=result,
            description=description,
            error_code=error_code,
            migrate_to_chat_id=migrate_to_chat_id,
            retry_after=retry_after,
        )
        return response

    def _check_arguments(self, *args, **kwargs) -> None:
        build_update = getattr(self._handler, "build_update", None)
        if build_update is None:
            return
        try:
            inspect.signature(build_update).bind(*args, **kwargs)
        except TypeError as e:
            raise AttributeError(f"incorrect argument name. {e}") from e
