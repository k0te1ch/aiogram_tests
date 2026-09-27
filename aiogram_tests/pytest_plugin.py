"""pytest fixtures, loaded automatically through the ``pytest11`` entry point"""

from collections.abc import Callable
from types import ModuleType
from typing import Any

import pytest
from aiogram import Dispatcher
from aiogram import Router

from .mocked_bot import MockedBot
from .tester import BotTester
from .types import dataset as _dataset


@pytest.fixture
def mocked_bot() -> MockedBot:
    return MockedBot()


@pytest.fixture
def bot_tester(mocked_bot: MockedBot) -> Callable[..., BotTester]:
    """
    Factory: ``bot_tester(router_or_dispatcher, **workflow_data)``; every tester in a test shares ``mocked_bot``
    """

    def make(dispatcher: Dispatcher | Router, **kwargs: Any) -> BotTester:
        kwargs.setdefault("bot", mocked_bot)
        return BotTester(dispatcher, **kwargs)

    return make


@pytest.fixture
def dataset() -> ModuleType:
    return _dataset
