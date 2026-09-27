import pytest
from aiogram import Bot
from aiogram.methods import AnswerPreCheckoutQuery
from aiogram.methods import SendMessage

from aiogram_tests.handler import ChannelPostHandler
from aiogram_tests.handler import ChatJoinRequestHandler
from aiogram_tests.handler import ChatMemberHandler
from aiogram_tests.handler import ChosenInlineResultHandler
from aiogram_tests.handler import EditedChannelPostHandler
from aiogram_tests.handler import EditedMessageHandler
from aiogram_tests.handler import InlineQueryHandler
from aiogram_tests.handler import MessageReactionHandler
from aiogram_tests.handler import MyChatMemberHandler
from aiogram_tests.handler import PollAnswerHandler
from aiogram_tests.handler import PollHandler
from aiogram_tests.handler import PreCheckoutQueryHandler
from aiogram_tests.handler import ShippingQueryHandler
from aiogram_tests.handler import UpdateHandler
from aiogram_tests.requester import MockedRequester
from aiogram_tests.types import dataset


async def report(event, bot: Bot):
    await bot.send_message(chat_id=1, text=type(event).__name__)


@pytest.mark.parametrize(
    ("handler_class", "item"),
    [
        (EditedMessageHandler, dataset.EDITED_MESSAGE),
        (ChannelPostHandler, dataset.CHANNEL_POST),
        (EditedChannelPostHandler, dataset.EDITED_CHANNEL_POST),
        (InlineQueryHandler, dataset.INLINE_QUERY),
        (ChosenInlineResultHandler, dataset.CHOSEN_INLINE_RESULT),
        (ShippingQueryHandler, dataset.SHIPPING_QUERY),
        (PreCheckoutQueryHandler, dataset.PRE_CHECKOUT_QUERY),
        (PollHandler, dataset.POLL),
        (PollAnswerHandler, dataset.POLL_ANSWER),
        (MyChatMemberHandler, dataset.CHAT_MEMBER_UPDATED),
        (ChatMemberHandler, dataset.CHAT_MEMBER_UPDATED),
        (ChatJoinRequestHandler, dataset.CHAT_JOIN_REQUEST),
        (MessageReactionHandler, dataset.MESSAGE_REACTION_UPDATED),
    ],
)
async def test_handler_receives_its_update_type(handler_class, item):
    requester = MockedRequester(handler_class(report))
    event = item.as_object()

    positional = await requester.query(event)
    by_name = await requester.query(**{handler_class.event: event})

    assert positional.last(SendMessage).text == type(event).__name__
    assert by_name.last(SendMessage).text == type(event).__name__


async def test_pre_checkout_query_can_be_answered():
    async def approve(query):
        await query.answer(ok=True)

    calls = await MockedRequester(PreCheckoutQueryHandler(approve)).query(dataset.PRE_CHECKOUT_QUERY.as_object())

    assert calls.assert_called(AnswerPreCheckoutQuery, ok=True)


async def test_update_handler_takes_the_event_name():
    requester = MockedRequester(UpdateHandler(report, event="edited_message"))

    calls = await requester.query(edited_message=dataset.EDITED_MESSAGE.as_object())

    assert calls.last(SendMessage).text == "Message"


@pytest.mark.parametrize("event", ["no_such_update", "update", "error"])
def test_update_handler_rejects_unknown_events(event):
    with pytest.raises(ValueError, match=event):
        UpdateHandler(report, event=event)


async def test_wrong_event_name_is_reported():
    requester = MockedRequester(InlineQueryHandler(report))

    with pytest.raises(AttributeError, match="inline_query"):
        await requester.query(message=dataset.INLINE_QUERY.as_object())


async def test_each_update_gets_its_own_id():
    seen = []

    async def remember(event, event_update):
        seen.append(event_update.update_id)

    handler = EditedMessageHandler(remember)
    await handler(dataset.EDITED_MESSAGE.as_object())
    await handler(dataset.EDITED_MESSAGE.as_object())

    assert seen[0] < seen[1]
