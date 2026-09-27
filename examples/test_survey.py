from aiogram.methods import AnswerCallbackQuery
from aiogram.methods import SendMessage
from survey_bot import Survey
from survey_bot import router


async def test_survey(bot_tester):
    tester = bot_tester(router, banned=set(), greeting="Nice to meet you")

    calls = await tester.send_message("/survey")
    calls.assert_called(SendMessage, text="What is your name?")
    assert await tester.get_state() == Survey.name

    await tester.send_message("Alice")
    calls = await tester.press("Python")

    calls.assert_called(AnswerCallbackQuery)
    calls.assert_called(SendMessage, text="Nice to meet you, Alice! python it is")
    assert await tester.get_state() is None


async def test_banned_user(bot_tester, dataset):
    alice = dataset.USER.as_object(id=7)
    tester = bot_tester(router, banned={7}, greeting="Hi")

    calls = await tester.send_message("/survey", user=alice)

    calls.assert_called(SendMessage, text="You are banned")
    assert await tester.get_state(alice) is None
