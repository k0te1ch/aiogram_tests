import itertools
from collections.abc import Callable
from collections.abc import Iterable
from typing import Any

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
    """
    Registers ``callback`` on the dispatcher observer ``event`` (``message``, ``inline_query``, ...) and feeds it
    updates of that type. Subclasses fix ``event``; ``UpdateHandler`` takes it as an argument.
    """

    event: str | None = None

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
        self._update_ids = itertools.count(1)

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

        return await self.dp.feed_update(self.bot, update)

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

        getattr(self.dp, self.event).register(self._callback, *self._filters)

    def build_update(self, *args, **kwargs) -> types.Update:
        """
        Wrap the event, passed positionally or by its update field name, into an update for the dispatcher
        """

        event = self._pick_event(args, kwargs)
        return types.Update(update_id=next(self._update_ids), **{self.event: event})

    def _pick_event(self, args: tuple, kwargs: dict) -> Any:
        if args and not kwargs:
            return args[0]
        if not args and list(kwargs) == [self.event]:
            return kwargs[self.event]
        passed = [*(type(arg).__name__ for arg in args), *kwargs]
        raise TypeError(f"{type(self).__name__} takes one '{self.event}' event, got {passed}")


class UpdateHandler(TelegramEventObserverHandler):
    """
    Handler for any update type by its field name: ``UpdateHandler(callback, event="business_message")``
    """

    def __init__(self, callback: Callable, *filters: Filter, event: str, **kwargs):
        self.event = event
        super().__init__(callback, *filters, **kwargs)
        if event not in self.dp.observers or event in ("update", "error"):
            raise ValueError(f"dispatcher has no '{event}' updates")


class MessageHandler(TelegramEventObserverHandler):
    event = "message"


class EditedMessageHandler(TelegramEventObserverHandler):
    event = "edited_message"


class ChannelPostHandler(TelegramEventObserverHandler):
    event = "channel_post"


class EditedChannelPostHandler(TelegramEventObserverHandler):
    event = "edited_channel_post"


class CallbackQueryHandler(TelegramEventObserverHandler):
    event = "callback_query"


class InlineQueryHandler(TelegramEventObserverHandler):
    event = "inline_query"


class ChosenInlineResultHandler(TelegramEventObserverHandler):
    event = "chosen_inline_result"


class ShippingQueryHandler(TelegramEventObserverHandler):
    event = "shipping_query"


class PreCheckoutQueryHandler(TelegramEventObserverHandler):
    event = "pre_checkout_query"


class PollHandler(TelegramEventObserverHandler):
    event = "poll"


class PollAnswerHandler(TelegramEventObserverHandler):
    event = "poll_answer"


class MyChatMemberHandler(TelegramEventObserverHandler):
    event = "my_chat_member"


class ChatMemberHandler(TelegramEventObserverHandler):
    event = "chat_member"


class ChatJoinRequestHandler(TelegramEventObserverHandler):
    event = "chat_join_request"


class MessageReactionHandler(TelegramEventObserverHandler):
    event = "message_reaction"
