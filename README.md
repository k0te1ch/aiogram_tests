# Aiogram Tests

***aiogram_tests*** is a testing library for bots written on [aiogram](https://github.com/aiogram/aiogram)

## 📦 Installation

```bash
pip install aiogram-testing
```

The import name stays `aiogram_tests`:

```python
from aiogram_tests import MockedRequester
```

## 📚 Simple examples

### Simple handler test

#### Simple bot

```python
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext

# Please, keep your bot tokens on environments, this code only example
bot = Bot('123456789:AABBCCDDEEFFaabbccddeeff-1234567890')
dp = Dispatcher()


@dp.message()
async def echo(message: types.Message, state: FSMContext) -> None:
    await message.answer(message.text)


if __name__ == '__main__':
    dp.run_polling(bot)


```

#### Test cases

```python
import pytest

from bot import echo

from aiogram_tests import MockedRequester
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import MESSAGE


@pytest.mark.asyncio
async def test_echo():
    request = MockedRequester(MessageHandler(echo))
    calls = await request.query(message=MESSAGE.as_object(text="Hello, Bot!"))
    answer_message = calls.send_message.fetchone()
    assert answer_message.text == "Hello, Bot!"

```

### Checking calls

`query()` returns the Bot API methods the handler called, as aiogram objects (`SendMessage`, `EditMessageText`, ...),
so fields such as `reply_markup` are typed models, not raw dicts.

```python
from aiogram.methods import AnswerCallbackQuery, SendMessage

calls = await request.query(message=MESSAGE.as_object(text="Hello, Bot!"))

calls.send_message.fetchone()            # last SendMessage, by snake_case name
calls.get(SendMessage)                   # all SendMessage calls, typed
calls.last(SendMessage)                  # last one or None
calls.assert_called(SendMessage, text="Hello, Bot!")   # fails with the calls that were made
calls.assert_not_called(AnswerCallbackQuery)
```

Accessing a method that was not called (`calls.edit_message_text`) raises `MethodIsNotCalledError`, an
`AttributeError`, so `hasattr(calls, "edit_message_text")` works. `calls.result` is what the dispatcher returned for
the update (a handler's return value, or `UNHANDLED` when nothing matched).

### Bot API answers and failures

With `auto_mock_success` on (the default) the bot answers like Telegram would: `send_message` returns a `Message`
with a fresh `message_id`, the target chat and the text; edits return the edited message (or `True` for inline
messages); boolean methods return `True`; `get_me` returns the bot. Queue a specific answer or a failure with
`add_result_for`; queued answers are used first, in order:

```python
from aiogram.exceptions import TelegramBadRequest, TelegramRetryAfter

bot.add_result_for(SendMessage, ok=False, error_code=400, description="Bad Request: chat not found")
bot.add_result_for(SendMessage, ok=False, error_code=429, description="Too Many Requests", retry_after=3)
```

Code that talks to the bot outside the dispatcher (background jobs, notifiers) can use a `MockedBot` directly;
`bot.calls` holds every call it made.

### Testing a whole router: `BotTester`

`MockedRequester` checks one handler function. `BotTester` runs updates through your real router or dispatcher, with
its filters, middlewares, FSM and injected dependencies, just like production:

```python
from aiogram.methods import SendMessage

from mybot.handlers import router


async def test_survey(bot_tester):  # fixture from the bundled pytest plugin
    tester = bot_tester(router, db=fake_db)   # keyword arguments reach handlers like dp.start_polling(**kwargs)

    calls = await tester.send_message("/survey")
    calls.assert_called(SendMessage, text="What is your name?")

    await tester.send_message("Alice")        # FSM state carries over between steps
    calls = await tester.press("Python")      # presses a button from the last inline keyboard

    calls.assert_called(SendMessage, text="Nice to meet you, Alice!")
    assert await tester.get_state() is None
```

- `send_message(text, user=..., chat=...)`, `click(data_or_callback_data, message=..., user=...)`, `press(button_text)`
  and `feed(event_or_update, event_type=...)` return the calls made while handling that update.
- `get_state(user)`, `set_state(state, user=..., **data)` and `state(user)` give access to the FSM.
- A module-level router is detached from the previous test's dispatcher, so each test gets a fresh one.
- A `Dispatcher` is used as is; its `workflow_data` and middlewares stay in place.

The plugin is registered automatically on install and provides the `bot_tester` (factory), `mocked_bot` and
`dataset` fixtures. See [examples/test_survey.py](examples/test_survey.py).

### Other update types

Each update type has its handler; pass the event positionally or by its update field name:

```python
from aiogram_tests.handler import InlineQueryHandler, PreCheckoutQueryHandler, UpdateHandler
from aiogram_tests.types.dataset import INLINE_QUERY, PRE_CHECKOUT_QUERY

calls = await MockedRequester(InlineQueryHandler(search)).query(INLINE_QUERY.as_object(query="cats"))
calls = await MockedRequester(PreCheckoutQueryHandler(approve)).query(pre_checkout_query=PRE_CHECKOUT_QUERY.as_object())

# anything else the dispatcher knows, by name
calls = await MockedRequester(UpdateHandler(on_business, event="business_message")).query(message)
```

Available: `MessageHandler`, `EditedMessageHandler`, `ChannelPostHandler`, `EditedChannelPostHandler`,
`CallbackQueryHandler`, `InlineQueryHandler`, `ChosenInlineResultHandler`, `ShippingQueryHandler`,
`PreCheckoutQueryHandler`, `PollHandler`, `PollAnswerHandler`, `MyChatMemberHandler`, `ChatMemberHandler`,
`ChatJoinRequestHandler`, `MessageReactionHandler` and `UpdateHandler`.

Middlewares passed as `dp_middlewares` are registered on every event observer except `update` and `error`, whose
events are `Update` and `ErrorEvent` rather than messages or callbacks.

### [▶️ More](https://github.com/k0te1ch/aiogram_tests/tree/main/examples) examples
