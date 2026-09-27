import pytest
from aiogram import types

from aiogram_tests.exceptions import MockedResponseMissingError
from aiogram_tests.handler import MessageHandler
from aiogram_tests.requester import MockedRequester
from aiogram_tests.types.dataset import CHAT
from aiogram_tests.types.dataset import MESSAGE
from aiogram_tests.types.dataset import USER

from .bot import States
from .bot import message_handler
from .bot import message_handler_with_state


async def noop(*args, **kwargs):
    pass


async def test_repeated_calls_register_handler_once():
    handler = MessageHandler(noop, state=States.state)
    await handler(MESSAGE.as_object())
    await handler(MESSAGE.as_object())

    assert len(handler.dp.message.handlers) == 1
    assert len(handler.dp.message.handlers[0].filters) == 1


async def test_state_is_set_for_the_event_sender():
    message = MESSAGE.as_object(from_user=USER.as_object(id=42), chat=CHAT.as_object(id=42))
    requester = MockedRequester(MessageHandler(message_handler_with_state, state=States.state))

    calls = await requester.query(message)

    assert calls.send_message.fetchone().text == "Hello, from state!"


async def test_missing_mocked_response_names_the_method():
    requester = MockedRequester(MessageHandler(message_handler, auto_mock_success=False))

    with pytest.raises(MockedResponseMissingError, match="sendMessage"):
        await requester.query(MESSAGE.as_object(text="Hello!"))


async def test_query_returns_only_its_own_calls():
    requester = MockedRequester(MessageHandler(message_handler))

    await requester.query(MESSAGE.as_object(text="one"))
    calls = await requester.query(MESSAGE.as_object(text="two"))

    assert [call.text for call in calls.send_message.fetchall()] == ["two"]


async def test_type_error_inside_handler_is_not_masked():
    async def broken(message: types.Message):
        raise TypeError("boom")

    requester = MockedRequester(MessageHandler(broken))

    with pytest.raises(TypeError, match="boom"):
        await requester.query(MESSAGE.as_object())


async def test_wrong_argument_name_still_raises_attribute_error():
    requester = MockedRequester(MessageHandler(noop))

    with pytest.raises(AttributeError, match="incorrect argument name"):
        await requester.query(callback_query=MESSAGE.as_object())
