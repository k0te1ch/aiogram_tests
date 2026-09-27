import pytest
from aiogram import Router
from aiogram import types
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.exceptions import TelegramBadRequest
from aiogram.exceptions import TelegramRetryAfter
from aiogram.methods import EditMessageText
from aiogram.methods import SendMessage

from aiogram_tests import BotTester
from aiogram_tests import MockedBot
from aiogram_tests import MockedRequester
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import MESSAGE


async def test_sent_messages_come_back_as_messages():
    bot = MockedBot()

    first = await bot.send_message(chat_id=7, text="hello")
    second = await bot.send_message(chat_id=7, text="again")

    assert isinstance(first, types.Message)
    assert (first.chat.id, first.text, first.from_user.id) == (7, "hello", bot.id)
    assert second.message_id == first.message_id + 1


async def test_edits_keep_the_message_id():
    bot = MockedBot()

    edited = await bot.edit_message_text(text="new", chat_id=7, message_id=41)
    inline = await bot.edit_message_text(text="new", inline_message_id="abc")

    assert (edited.message_id, edited.text) == (41, "new")
    assert inline is True


async def test_boolean_and_bot_methods():
    bot = MockedBot()

    assert await bot.answer_callback_query("id") is True
    assert (await bot.get_me()).id == bot.id
    assert await bot.get_updates() == []


async def test_queued_failure_is_not_followed_by_a_stale_success():
    bot = MockedBot()
    bot.add_result_for(SendMessage, ok=False, error_code=400, description="Bad Request: chat not found")

    with pytest.raises(TelegramBadRequest, match="chat not found"):
        await bot.send_message(chat_id=7, text="x")

    assert await bot.delete_message(chat_id=7, message_id=1) is True


async def test_flood_control_raises_retry_after():
    bot = MockedBot()
    bot.add_result_for(SendMessage, ok=False, error_code=429, description="Too Many Requests", retry_after=3)

    with pytest.raises(TelegramRetryAfter) as error:
        await bot.send_message(chat_id=7, text="x")

    assert error.value.retry_after == 3


async def test_bot_records_calls_made_outside_the_dispatcher():
    bot = MockedBot()

    await bot.send_message(chat_id=7, text="report")
    await bot.edit_message_text(text="report v2", chat_id=7, message_id=1)

    assert bot.calls.last(EditMessageText).text == "report v2"
    assert len(bot.calls) == 2


async def test_calls_carry_the_dispatcher_result():
    router = Router()

    @router.message()
    async def pong(message: types.Message) -> str:
        return "pong"

    tester = BotTester(router)

    assert (await tester.send_message("ping")).result == "pong"
    assert (await tester.feed(types.CallbackQuery(id="1", from_user=tester.user, chat_instance="x"))).result is (
        UNHANDLED
    )


async def test_requester_calls_carry_the_result():
    async def pong(message: types.Message) -> str:
        return "pong"

    calls = await MockedRequester(MessageHandler(pong)).query(MESSAGE.as_object())

    assert calls.result == "pong"
