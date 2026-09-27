"""Keyboards and webhook info"""

from aiogram import types

from .base import DatasetItem

WEBHOOK_INFO = DatasetItem(
    {
        "url": "",
        "has_custom_certificate": False,
        "pending_update_count": 0,
    },
    model=types.WebhookInfo,
)

REPLY_KEYBOARD_MARKUP = DatasetItem(
    {
        "keyboard": [[{"text": "something here"}]],
        "resize_keyboard": True,
    },
    model=types.ReplyKeyboardMarkup,
)
