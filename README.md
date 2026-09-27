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
`AttributeError`, so `hasattr(calls, "edit_message_text")` works.

### [▶️ More](https://github.com/k0te1ch/aiogram_tests/tree/main/examples) examples
