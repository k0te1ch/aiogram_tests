"""Message entities and bot commands"""

from aiogram import types

from .base import DatasetItem

BOT_COMMAND = DatasetItem(
    {
        "command": "start",
        "description": "Start bot",
    },
    model=types.BotCommand,
)

ENTITY_BOLD = DatasetItem(
    {
        "offset": 5,
        "length": 2,
        "type": "bold",
    },
    model=types.MessageEntity,
)

ENTITY_ITALIC = DatasetItem(
    {
        "offset": 8,
        "length": 1,
        "type": "italic",
    },
    model=types.MessageEntity,
)

ENTITY_LINK = DatasetItem(
    {
        "offset": 10,
        "length": 6,
        "type": "text_link",
        "url": "https://google.com/",
    },
    model=types.MessageEntity,
)

ENTITY_CODE = DatasetItem(
    {
        "offset": 17,
        "length": 7,
        "type": "code",
    },
    model=types.MessageEntity,
)

ENTITY_PRE = DatasetItem(
    {
        "offset": 30,
        "length": 4,
        "type": "pre",
    },
    model=types.MessageEntity,
)

ENTITY_MENTION = DatasetItem(
    {
        "offset": 47,
        "length": 9,
        "type": "mention",
    },
    model=types.MessageEntity,
)
