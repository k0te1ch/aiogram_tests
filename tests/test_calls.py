import pytest
from aiogram import types
from aiogram.methods import AnswerCallbackQuery
from aiogram.methods import SendMessage
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram_tests.handler import MessageHandler
from aiogram_tests.requester import MockedRequester
from aiogram_tests.types.dataset import MESSAGE


async def greet(message: types.Message):
    keyboard = InlineKeyboardBuilder().button(text="OK", callback_data="ok").as_markup()
    await message.answer("first")
    await message.answer("second", reply_markup=keyboard)


@pytest.fixture
async def calls():
    return await MockedRequester(MessageHandler(greet)).query(MESSAGE.as_object())


async def test_calls_are_aiogram_methods(calls):
    call = calls.send_message.fetchone()

    assert isinstance(call, SendMessage)
    assert isinstance(call.reply_markup, types.InlineKeyboardMarkup)
    assert call.reply_markup.inline_keyboard[0][0].callback_data == "ok"


async def test_typed_access(calls):
    assert [call.text for call in calls.get(SendMessage)] == ["first", "second"]
    assert calls.last(SendMessage).text == "second"
    assert calls.get(AnswerCallbackQuery) == []
    assert calls.last(AnswerCallbackQuery) is None
    assert len(calls) == 2
    assert [type(call) for call in calls] == [SendMessage, SendMessage]


async def test_assert_called_returns_the_matching_call(calls):
    call = calls.assert_called(SendMessage, text="first")

    assert call.text == "first"


async def test_assert_called_lists_the_calls_made(calls):
    with pytest.raises(AssertionError, match=r"SendMessage\(text='third'\) was not called(.|\n)*second"):
        calls.assert_called(SendMessage, text="third")


async def test_assert_not_called(calls):
    calls.assert_not_called(AnswerCallbackQuery)

    with pytest.raises(AssertionError, match="called 2 time"):
        calls.assert_not_called(SendMessage)


async def test_missing_method_is_an_attribute_error(calls):
    assert not hasattr(calls, "edit_message_text")
