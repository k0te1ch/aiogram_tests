"""A router with a middleware, dependency injection and a two-step FSM survey"""

from collections.abc import Awaitable
from collections.abc import Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram import F
from aiogram import Router
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


class Survey(StatesGroup):
    name = State()
    language = State()


class BannedUsers(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: types.Message,
        data: dict[str, Any],
    ) -> Any:
        if event.from_user.id in data["banned"]:
            return await event.answer("You are banned")
        return await handler(event, data)


router.message.middleware(BannedUsers())


@router.message(Command("survey"))
async def start(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Survey.name)
    await message.answer("What is your name?")


@router.message(Survey.name)
async def name(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(Survey.language)
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Python", callback_data="lang:python")
    keyboard.button(text="Go", callback_data="lang:go")
    await message.answer("Pick a language", reply_markup=keyboard.as_markup())


@router.callback_query(Survey.language, F.data.startswith("lang:"))
async def language(callback: types.CallbackQuery, state: FSMContext, greeting: str) -> None:
    data = await state.get_data()
    await state.clear()
    await callback.answer()
    await callback.message.answer(f"{greeting}, {data['name']}! {callback.data.removeprefix('lang:')} it is")
