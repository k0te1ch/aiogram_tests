import itertools
from typing import Any

from aiogram import Dispatcher
from aiogram import Router
from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.methods import TelegramMethod
from aiogram.methods.base import Response
from aiogram.methods.base import TelegramType

from .mocked_bot import DEFAULT_AUTO_MOCK_SUCCESS
from .mocked_bot import MockedBot
from .requester import Calls
from .types.dataset import CALLBACK_QUERY
from .types.dataset import CHAT
from .types.dataset import MESSAGE
from .types.dataset import USER

# Update fields by the event type they carry; a Message defaults to "message"
_EVENT_FIELDS: dict[type, str] = {}
for _name, _field in types.Update.model_fields.items():
    _annotation = getattr(_field.annotation, "__args__", (_field.annotation,))[0]
    if isinstance(_annotation, type):
        _EVENT_FIELDS.setdefault(_annotation, _name)


class BotTester:
    """
    Runs updates through a real dispatcher or router, with its filters, middlewares and FSM, against a mocked bot.

    ``workflow_data`` is passed to handlers the same way ``dp.start_polling(bot, **kwargs)`` passes it.
    """

    def __init__(
        self,
        dispatcher: Dispatcher | Router,
        *,
        bot: MockedBot | None = None,
        auto_mock_success: bool = DEFAULT_AUTO_MOCK_SUCCESS,
        user: types.User | None = None,
        chat: types.Chat | None = None,
        **workflow_data: Any,
    ):
        self.bot = bot or MockedBot(auto_mock_success=auto_mock_success)
        self.dp = dispatcher if isinstance(dispatcher, Dispatcher) else self._wrap(dispatcher)
        self.user = user or USER.as_object()
        self.chat = chat or CHAT.as_object(id=self.user.id)
        self._workflow_data = workflow_data
        self._update_ids = itertools.count(1)
        self._message_ids = itertools.count(1)
        self._last_calls = Calls()

    @staticmethod
    def _wrap(router: Router) -> Dispatcher:
        # A module-level router stays attached to the dispatcher of the previous test; detach it first
        parent = router.parent_router
        if parent is not None:
            parent.sub_routers.remove(router)
            router._parent_router = None
        dp = Dispatcher(storage=MemoryStorage())
        dp.include_router(router)
        return dp

    async def feed(self, event: types.TelegramObject, *, event_type: str | None = None) -> Calls:
        """
        Feed an update or a bare event; ``event_type`` picks the update field when the type is ambiguous
        (``edited_message`` for a Message)
        """

        if isinstance(event, types.Update):
            update = event
        else:
            field = event_type or _EVENT_FIELDS.get(type(event))
            if field is None:
                raise TypeError(f"no update field for {type(event).__name__}; pass event_type=")
            update = types.Update(update_id=next(self._update_ids), **{field: event})

        methods = self.bot.session.methods
        already_made = len(methods)
        await self.dp.feed_update(self.bot, update, **self._workflow_data)
        self._last_calls = Calls(list(methods)[already_made:])
        return self._last_calls

    async def send_message(
        self, text: str, *, user: types.User | None = None, chat: types.Chat | None = None, **fields: Any
    ) -> Calls:
        user = user or self.user
        message = MESSAGE.as_object(
            message_id=next(self._message_ids),
            text=text,
            from_user=user,
            chat=chat or (self.chat if user is self.user else CHAT.as_object(id=user.id)),
            **fields,
        )
        return await self.feed(message)

    async def click(
        self,
        data: str | CallbackData,
        *,
        message: types.Message | None = None,
        user: types.User | None = None,
    ) -> Calls:
        """
        Send a callback query with ``data``, as if the user pressed a button under ``message``
        """

        user = user or self.user
        callback_query = CALLBACK_QUERY.as_object(
            id=str(next(self._update_ids)),
            data=data.pack() if isinstance(data, CallbackData) else data,
            from_user=user,
            message=message or MESSAGE.as_object(message_id=next(self._message_ids), chat=self.chat, from_user=user),
        )
        return await self.feed(callback_query)

    async def press(self, text: str, *, user: types.User | None = None) -> Calls:
        """
        Press the inline button labelled ``text`` in the last keyboard the bot sent
        """

        keyboard = self._last_inline_keyboard()
        labels = [button.text for row in keyboard for button in row]
        for row in keyboard:
            for button in row:
                if button.text == text:
                    if button.callback_data is None:
                        raise ValueError(f"button {text!r} has no callback data")
                    return await self.click(button.callback_data, user=user)
        raise LookupError(f"no button {text!r} in the last inline keyboard; buttons: {labels}")

    def _last_inline_keyboard(self) -> list[list[types.InlineKeyboardButton]]:
        for call in reversed(list(self._last_calls)):
            markup = getattr(call, "reply_markup", None)
            if isinstance(markup, types.InlineKeyboardMarkup):
                return markup.inline_keyboard
        raise LookupError("the bot sent no inline keyboard in the last update")

    def state(self, user: types.User | None = None, chat: types.Chat | None = None) -> FSMContext:
        user = user or self.user
        chat = chat or (self.chat if user is self.user else CHAT.as_object(id=user.id))
        return self.dp.fsm.resolve_context(bot=self.bot, chat_id=chat.id, user_id=user.id)

    async def get_state(self, user: types.User | None = None) -> str | None:
        return await self.state(user).get_state()

    async def set_state(self, state: State | str | None, *, user: types.User | None = None, **data: Any) -> None:
        context = self.state(user)
        await context.set_state(state)
        if data:
            await context.update_data(**data)

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
        return self.bot.add_result_for(
            method=method,
            ok=ok,
            result=result,
            description=description,
            error_code=error_code,
            migrate_to_chat_id=migrate_to_chat_id,
            retry_after=retry_after,
        )
