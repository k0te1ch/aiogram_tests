import pytest
from aiogram.filters import StateFilter

from aiogram_tests.handler import MessageHandler
from aiogram_tests.handler import RequestHandler
from aiogram_tests.handler import TelegramEventObserverHandler
from aiogram_tests.types.dataset import MESSAGE

from .middleware import TestMiddleware


def test_request_handler_initialization():
    RequestHandler((), ())


def test_request_handler_dp_middlewares():
    r_h = RequestHandler(dp_middlewares=(TestMiddleware(),))
    middlewares_count = len(r_h.dp.message.middleware)
    assert middlewares_count == 1

    r_h = RequestHandler(dp_middlewares=(TestMiddleware(), TestMiddleware()))
    middlewares_count = len(r_h.dp.message.middleware)
    assert middlewares_count == 2

    r_h = RequestHandler(dp_middlewares=(TestMiddleware(), TestMiddleware()), exclude_observer_methods=["message"])
    middlewares_count = len(r_h.dp.message.middleware)
    assert middlewares_count == 0


def test_telegram_observ_methods_handler_init():
    async def callback(*args, **kwargs):
        pass

    with pytest.raises(ValueError):
        _ = TelegramEventObserverHandler(callback, state_data=[])


@pytest.mark.asyncio
async def test_telegram_observ_handler():
    async def callback(*args, **kwargs):
        pass

    t_h = MessageHandler(callback)
    await t_h(MESSAGE.as_object())
    handlers_count = len(t_h.dp.message.handlers)
    assert handlers_count == 1

    t_h = MessageHandler(callback, StateFilter(None))
    await t_h(MESSAGE.as_object())
    handlers_count = len(t_h.dp.message.handlers)
    assert handlers_count == 1


@pytest.mark.asyncio
async def test_state_telegram_observ_handler():
    async def callback(*args, **kwargs):
        pass

    t_h = MessageHandler(callback, state="state", state_data={"name": "Mike"})
    await t_h(MESSAGE.as_object())

    context = t_h.dp.fsm.get_context(t_h.bot, 12345678, 12345678)
    state = await context.get_state()
    data = await context.get_data()

    assert state == "state"
    assert data == {"name": "Mike"}


async def test_event_middlewares_skip_update_and_error_observers():
    seen = []

    class FromUserMiddleware(TestMiddleware):
        async def __call__(self, handler, event, data):
            seen.append(event.from_user.id)
            return await handler(event, data)

    async def callback(*args, **kwargs):
        pass

    handler = MessageHandler(callback, dp_middlewares=[FromUserMiddleware()])
    await handler(MESSAGE.as_object())

    assert len(handler.dp.update.middleware) == 0
    assert len(handler.dp.errors.middleware) == 0
    assert seen == [MESSAGE.as_object().from_user.id]
