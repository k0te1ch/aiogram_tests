"""Messages of every kind, callback queries and updates"""

from aiogram import types

from .base import DatasetItem
from .chats import CHANNEL
from .chats import CHAT
from .chats import CHAT_LOCATION
from .chats import CHAT_PERMISSIONS
from .chats import CHAT_PHOTO
from .chats import USER
from .entities import ENTITY_BOLD
from .entities import ENTITY_CODE
from .entities import ENTITY_ITALIC
from .entities import ENTITY_LINK
from .entities import ENTITY_MENTION
from .entities import ENTITY_PRE
from .media import AUDIO
from .media import CONTACT
from .media import DICE
from .media import DOCUMENT
from .media import GAME
from .media import LOCATION
from .media import PHOTO
from .media import STICKER
from .media import VENUE
from .media import VIDEO
from .media import VIDEO_NOTE
from .media import VOICE
from .payments import INVOICE
from .payments import SUCCESSFUL_PAYMENT

MESSAGE = DatasetItem(
    {
        "message_id": 11223,
        "from": USER,
        "chat": CHAT,
        "date": 1508709711,
        "text": "Hi, world!",
    },
    model=types.Message,
)

CALLBACK_QUERY = DatasetItem(
    {"id": "12345678", "chat_instance": "AABBCC", "from_user": USER, "message": MESSAGE, "data": "data"},
    model=types.CallbackQuery,
)

CHANNEL_POST = DatasetItem(
    {"message_id": 12345, "sender_chat": CHANNEL, "chat": CHANNEL, "date": 1508825372, "text": "Hi, channel!"},
    model=types.Message,
)

EDITED_CHANNEL_POST = DatasetItem(
    {
        "message_id": 12345,
        "sender_chat": CHANNEL,
        "chat": CHANNEL,
        "date": 1508825372,
        "edit_date": 1508825379,
        "text": "Hi, channel! (edited)",
    },
    model=types.Message,
)

EDITED_MESSAGE = DatasetItem(
    {
        "message_id": 12345,
        "from": USER,
        "chat": CHAT,
        "date": 1508825372,
        "edit_date": 1508825379,
        "text": "hi there (edited)",
    },
    model=types.Message,
)

FORWARDED_MESSAGE = DatasetItem(
    {
        "message_id": 12345,
        "from": USER,
        "chat": CHAT,
        "date": 1522828529,
        "forward_from_chat": CHAT,
        "forward_from_message_id": 123,
        "forward_date": 1522749037,
        "text": "Forwarded text with entities from public channel ",
        "entities": [ENTITY_BOLD, ENTITY_CODE, ENTITY_ITALIC, ENTITY_LINK, ENTITY_LINK, ENTITY_MENTION, ENTITY_PRE],
    },
    model=types.Message,
)

MESSAGE_WITH_AUDIO = DatasetItem(
    {
        "message_id": 12345,
        "from": USER,
        "chat": CHAT,
        "date": 1508739776,
        "audio": AUDIO,
        "caption": "This is my favourite song",
    },
    model=types.Message,
)

MESSAGE_WITH_CONTACT = DatasetItem(
    {
        "message_id": 56006,
        "from": USER,
        "chat": CHAT,
        "date": 1522850298,
        "contact": CONTACT,
    },
    model=types.Message,
)

MESSAGE_WITH_DICE = DatasetItem(
    {"message_id": 12345, "from": USER, "chat": CHAT, "date": 1508768012, "dice": DICE}, model=types.Message
)

MESSAGE_WITH_DOCUMENT = DatasetItem(
    {
        "message_id": 12345,
        "from": USER,
        "chat": CHAT,
        "date": 1508768012,
        "document": DOCUMENT,
        "caption": "Read my document",
    },
    model=types.Message,
)

MESSAGE_WITH_GAME = DatasetItem(
    {
        "message_id": 12345,
        "from": USER,
        "chat": CHAT,
        "date": 1508824810,
        "game": GAME,
    },
    model=types.Message,
)

MESSAGE_WITH_INVOICE = DatasetItem(
    {
        "message_id": 9772,
        "from": USER,
        "chat": CHAT,
        "date": 1508761719,
        "invoice": INVOICE,
    },
    model=types.Message,
)

MESSAGE_WITH_LOCATION = DatasetItem(
    {
        "message_id": 12345,
        "from": USER,
        "chat": CHAT,
        "date": 1508755473,
        "location": LOCATION,
    },
    model=types.Message,
)

MESSAGE_WITH_MIGRATE_TO_CHAT_ID = DatasetItem(
    {
        "message_id": 12345,
        "from": USER,
        "chat": CHAT,
        "date": 1526943253,
        "migrate_to_chat_id": -1234567890987,
    },
    model=types.Message,
)

MESSAGE_WITH_MIGRATE_FROM_CHAT_ID = DatasetItem(
    {
        "message_id": 12345,
        "from": USER,
        "chat": CHAT,
        "date": 1526943253,
        "migrate_from_chat_id": -123456789,
    },
    model=types.Message,
)

MESSAGE_WITH_PHOTO = DatasetItem(
    {
        "message_id": 12345,
        "from": USER,
        "chat": CHAT,
        "date": 1508825154,
        "photo": [PHOTO, PHOTO, PHOTO, PHOTO],
        "caption": "photo description",
    },
    model=types.Message,
)

MESSAGE_WITH_MEDIA_GROUP = DatasetItem(
    {
        "message_id": 55966,
        "from": USER,
        "chat": CHAT,
        "date": 1522843665,
        "media_group_id": "12182749320567362",
        "photo": [PHOTO, PHOTO, PHOTO, PHOTO],
    },
    model=types.Message,
)

MESSAGE_WITH_STICKER = DatasetItem(
    {
        "message_id": 12345,
        "from": USER,
        "chat": CHAT,
        "date": 1508771450,
        "sticker": STICKER,
    },
    model=types.Message,
)

MESSAGE_WITH_SUCCESSFUL_PAYMENT = DatasetItem(
    {
        "message_id": 9768,
        "from": USER,
        "chat": CHAT,
        "date": 1508761169,
        "successful_payment": SUCCESSFUL_PAYMENT,
    },
    model=types.Message,
)

MESSAGE_WITH_VENUE = DatasetItem(
    {
        "message_id": 56004,
        "from": USER,
        "chat": CHAT,
        "date": 1522849819,
        "location": LOCATION,
        "venue": VENUE,
    },
    model=types.Message,
)

MESSAGE_WITH_VIDEO = DatasetItem(
    {
        "message_id": 12345,
        "from": USER,
        "chat": CHAT,
        "date": 1508756494,
        "video": VIDEO,
        "caption": "description",
    },
    model=types.Message,
)

MESSAGE_WITH_VIDEO_NOTE = DatasetItem(
    {
        "message_id": 55934,
        "from": USER,
        "chat": CHAT,
        "date": 1522835890,
        "video_note": VIDEO_NOTE,
    },
    model=types.Message,
)

MESSAGE_WITH_VOICE = DatasetItem(
    {
        "message_id": 12345,
        "from": USER,
        "chat": CHAT,
        "date": 1508768403,
        "voice": VOICE,
    },
    model=types.Message,
)

MESSAGE_FROM_CHANNEL = DatasetItem(
    {
        "message_id": 123432,
        "from": None,
        "chat": CHANNEL,
        "date": 1508768405,
        "text": "Hi, world!",
    },
    model=types.Message,
)

REPLY_MESSAGE = DatasetItem(
    {
        "message_id": 12345,
        "from": USER,
        "chat": CHAT,
        "date": 1508751866,
        "reply_to_message": MESSAGE,
        "text": "Reply to quoted message",
    },
    model=types.Message,
)

UPDATE = DatasetItem(
    {
        "update_id": 123456789,
        "message": MESSAGE,
    },
    model=types.Update,
)

FULL_CHAT = DatasetItem(
    {
        **CHAT,
        "photo": CHAT_PHOTO,
        "bio": "bio",
        "has_private_forwards": False,
        "description": "description",
        "invite_link": "invite_link",
        "pinned_message": MESSAGE,
        "permissions": CHAT_PERMISSIONS,
        "slow_mode_delay": 10,
        "message_auto_delete_time": 60,
        "has_protected_content": True,
        "sticker_set_name": "sticker_set_name",
        "can_set_sticker_set": True,
        "linked_chat_id": -1234567890,
        "location": CHAT_LOCATION,
    },
    model=types.Chat,
)
