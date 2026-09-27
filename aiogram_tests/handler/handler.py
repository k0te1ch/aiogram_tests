from collections.abc import Callable
from collections.abc import Iterable

from aiogram import types
from aiogram.dispatcher.middlewares.user_context import UserContextMiddleware
from aiogram.filters import Filter
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from aiogram_tests.types.dataset import CHAT
from aiogram_tests.types.dataset import USER

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

        if state_data is None:
            state_data = {}
        if not isinstance(state_data, dict):
            raise ValueError("state_data is not a dict")

        self._callback = callback
        self._filters: list = list(filters)
        self._state: State | str | None = state
        self._state_data: dict = state_data
        self._state_context: FSMContext | None = state_context
        self._registered = False

        if self._state:
            self._filters.append(StateFilter(self._state))

    async def __call__(self, *args, **kwargs):
        if not self._registered:
            self.register_handler()
            self._registered = True

        update = self.build_update(*args, **kwargs)

        if self._state_context or self._state:
            state = self._get_state_context(update)
            await state.set_state(self._state)
            await state.update_data(**self._state_data)

        await self.dp.feed_update(self.bot, update)

    def _get_state_context(self, update: types.Update) -> FSMContext:
        """
        FSM context of the user and chat the update comes from, as the dispatcher resolves it
        """

        context = UserContextMiddleware.resolve_event_context(update)
        state = self.dp.fsm.resolve_context(
            bot=self.bot,
            chat_id=context.chat_id or CHAT["id"],
            user_id=context.user_id or USER["id"],
            thread_id=context.thread_id,
            business_connection_id=context.business_connection_id,
        )
        return state

    def register_handler(self) -> None:
        """
        Register TelegramEventObserver in dispatcher
        """

        raise NotImplementedError

    def build_update(self, *args, **kwargs) -> types.Update:
        """
        Wrap the event into an update for the dispatcher
        """

        raise NotImplementedError


class MessageHandler(TelegramEventObserverHandler):
    def register_handler(self) -> None:
        self.dp.message.register(self._callback, *self._filters)

    def build_update(self, message: types.Message, *args, **kwargs) -> types.Update:
        return types.Update(update_id=12345678, message=message)


class CallbackQueryHandler(TelegramEventObserverHandler):
    def register_handler(self) -> None:
        self.dp.callback_query.register(self._callback, *self._filters)

    def build_update(self, callback_query: types.CallbackQuery, *args, **kwargs) -> types.Update:
        return types.Update(update_id=12345678, callback_query=callback_query)
