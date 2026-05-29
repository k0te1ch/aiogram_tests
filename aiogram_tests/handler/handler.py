from collections.abc import Callable
from collections.abc import Iterable

from aiogram import types
from aiogram.filters import Filter
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from .base import RequestHandler


class TelegramEventObserverHandler(RequestHandler):
    def __init__(
        self,
        callback: Callable,
        *filters: Filter,
        state: State | str | None = None,
        state_data: dict = None,
        state_context: FSMContext | None = None,
        dp_middlewares: Iterable = None,
        exclude_observer_methods: Iterable = None,
        **kwargs,
    ):
        super().__init__(dp_middlewares, exclude_observer_methods, **kwargs)

        self._callback = callback
        self._filters: list = list(filters)
        self._state: State | str | None = state
        self._state_data: dict = state_data
        self._state_context: FSMContext = state_context

        if self._state_context:
            self._state_context = state_context

        if self._state_data is None:
            self._state_data = {}

        if self._filters is None:
            self._filters = []

        if not isinstance(self._state_data, dict):
            raise ValueError("state_data is not a dict")

    async def __call__(self, *args, **kwargs):
        if self._state:
            self._filters.append(StateFilter(self._state))

        self.register_handler()

        if self._state_context or self._state:
            state = self.dp.fsm.get_context(self.bot, user_id=12345678, chat_id=12345678)
            await state.set_state(self._state)
            await state.update_data(**self._state_data)

        await self.feed_update(*args, **kwargs)

    def register_handler(self) -> None:
        """
        Register TelegramEventObserver in dispatcher
        """

        raise NotImplementedError

    async def feed_update(self, *args, **kwargs) -> None:
        """
        Feed dispatcher updates
        """

        raise NotImplementedError


class MessageHandler(TelegramEventObserverHandler):
    def register_handler(self) -> None:
        self.dp.message.register(self._callback, *self._filters)

    async def feed_update(self, message: types.Message, *args, **kwargs) -> None:
        await self.dp.feed_update(self.bot, types.Update(update_id=12345678, message=message))


class CallbackQueryHandler(TelegramEventObserverHandler):
    def register_handler(self) -> None:
        self.dp.callback_query.register(self._callback, *self._filters)

    async def feed_update(self, callback_query: types.CallbackQuery, *args, **kwargs) -> None:
        await self.dp.feed_update(self.bot, types.Update(update_id=12345678, callback_query=callback_query))
