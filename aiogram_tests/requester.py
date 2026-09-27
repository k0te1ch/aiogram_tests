from aiogram.methods import TelegramMethod
from aiogram.methods.base import Response
from aiogram.methods.base import TelegramType

from .calls import Calls
from .calls import CallsList
from .handler.base import RequestHandler

__all__ = ["Calls", "CallsList", "MockedRequester"]


class MockedRequester:
    def __init__(self, request_handler: RequestHandler):
        self._handler: RequestHandler = request_handler

    async def query(self, *args, **kwargs) -> Calls:
        self._check_arguments(*args, **kwargs)

        methods = self._handler.bot.session.methods
        already_made = len(methods)
        result = await self._handler(*args, **kwargs)

        return Calls(list(methods)[already_made:], result=result)

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
            build_update(*args, **kwargs)
        except TypeError as e:
            raise AttributeError(f"incorrect argument name. {e}") from e
