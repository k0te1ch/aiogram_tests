import pytest
from aiogram import Dispatcher
from aiogram import F
from aiogram import Router
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.methods import SendMessage
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram_tests import BotTester
from aiogram_tests.types import dataset

from .bot import TestCallbackData

router = Router()


@router.message(Command("menu"))
async def menu(message: types.Message) -> None:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Hello", callback_data=TestCallbackData(id=1, name="menu"))
    keyboard.button(text="Docs", url="https://docs.aiogram.dev")
    await message.answer("Menu", reply_markup=keyboard.as_markup())


@router.callback_query(TestCallbackData.filter())
async def hello(callback: types.CallbackQuery, callback_data: TestCallbackData) -> None:
    await callback.message.answer(f"Hello from {callback_data.name}, {callback.from_user.id}")


@router.message(Command("whoami"))
async def whoami(message: types.Message, owner: str) -> None:
    await message.answer(f"{message.from_user.id} owned by {owner}")


@router.edited_message(F.text)
async def edited(message: types.Message) -> None:
    await message.answer("edited")


@router.inline_query()
async def inline(query: types.InlineQuery) -> None:
    await query.bot.send_message(chat_id=query.from_user.id, text=f"inline: {query.query}")


async def test_router_can_be_tested_again_in_a_fresh_dispatcher():
    first = BotTester(router)
    second = BotTester(router)

    assert first.dp is not second.dp
    (await second.send_message("/menu")).assert_called(SendMessage, text="Menu")


async def test_dispatcher_is_used_as_is():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(Router())

    assert BotTester(dp).dp is dp


async def test_workflow_data_reaches_handlers():
    calls = await BotTester(router, owner="Alice").send_message("/whoami")

    calls.assert_called(SendMessage, text=f"{dataset.USER['id']} owned by Alice")


async def test_press_clicks_the_button_from_the_last_keyboard():
    tester = BotTester(router)
    await tester.send_message("/menu")

    calls = await tester.press("Hello")

    calls.assert_called(SendMessage, text=f"Hello from menu, {dataset.USER['id']}")


async def test_press_lists_available_buttons():
    tester = BotTester(router)
    await tester.send_message("/menu")

    with pytest.raises(LookupError, match=r"no button 'Bye'.*\['Hello', 'Docs'\]"):
        await tester.press("Bye")
    with pytest.raises(ValueError, match="no callback data"):
        await tester.press("Docs")


async def test_press_without_keyboard():
    with pytest.raises(LookupError, match="no inline keyboard"):
        await BotTester(router).press("Hello")


async def test_click_packs_callback_data_for_another_user():
    other = dataset.USER.as_object(id=42)

    calls = await BotTester(router).click(TestCallbackData(id=1, name="button"), user=other)

    calls.assert_called(SendMessage, text="Hello from button, 42")


async def test_feed_picks_the_update_field_by_event_type():
    tester = BotTester(router)

    inline_calls = await tester.feed(dataset.INLINE_QUERY.as_object(query="cats"))
    edited_calls = await tester.feed(dataset.MESSAGE.as_object(), event_type="edited_message")
    update_calls = await tester.feed(types.Update(update_id=99, inline_query=dataset.INLINE_QUERY.as_object()))

    inline_calls.assert_called(SendMessage, text="inline: cats")
    edited_calls.assert_called(SendMessage, text="edited")
    assert len(update_calls) == 1


async def test_feed_rejects_unknown_events():
    with pytest.raises(TypeError, match="event_type"):
        await BotTester(router).feed(dataset.USER.as_object())


async def test_state_is_kept_per_user():
    tester = BotTester(router)
    other = dataset.USER.as_object(id=42)

    await tester.set_state("waiting", note="first")
    await tester.set_state("other", user=other)

    assert await tester.get_state() == "waiting"
    assert await tester.state().get_data() == {"note": "first"}
    assert await tester.get_state(other) == "other"


async def test_calls_belong_to_one_update():
    tester = BotTester(router)
    await tester.send_message("/menu")

    calls = await tester.send_message("/menu")

    assert len(calls) == 1


async def test_fixtures(bot_tester, mocked_bot, dataset):
    tester = bot_tester(router)

    assert tester.bot is mocked_bot
    assert dataset.MESSAGE.as_object().text
