"""Users, chats and chat members"""

from aiogram import types

from .base import DatasetItem
from .media import LOCATION
from .media import PHOTO

USER = DatasetItem(
    {
        "id": 12345678,
        "is_bot": False,
        "first_name": "FirstName",
        "last_name": "LastName",
        "username": "username",
        "language_code": "ru",
    },
    model=types.User,
)

CHAT = DatasetItem(
    {
        "id": 12345678,
        "first_name": "FirstName",
        "last_name": "LastName",
        "username": "username",
        "type": "private",
    },
    model=types.Chat,
)

CHAT_PHOTO = DatasetItem(
    {
        "small_file_id": "small_file_id",
        "small_file_unique_id": "small_file_unique_id",
        "big_file_id": "big_file_id",
        "big_file_unique_id": "big_file_unique_id",
    },
    model=types.ChatPhoto,
)

CHAT_MEMBER = DatasetItem(
    {
        "user": USER,
        "status": "administrator",
        "can_be_edited": False,
        "can_manage_chat": True,
        "can_change_info": True,
        "can_delete_messages": True,
        "can_invite_users": True,
        "can_restrict_members": True,
        "can_pin_messages": True,
        "can_promote_members": False,
        "can_manage_voice_chats": True,  # Deprecated
        "can_manage_video_chats": True,
        "is_anonymous": False,
    },
    model=types.ChatMember,
)

CHAT_MEMBER_OWNER = DatasetItem(
    {
        "user": USER,
        "status": "creator",
        "is_anonymous": False,
    },
    model=types.ChatMemberOwner,
)

CHANNEL = DatasetItem(
    {
        "type": "channel",
        "username": "best_channel_ever",
        "id": -1001065170817,
    },
    model=types.Chat,
)

USER_PROFILE_PHOTOS = DatasetItem(
    {
        "total_count": 1,
        "photos": [
            [PHOTO, PHOTO, PHOTO],
        ],
    },
    model=types.UserProfilePhotos,
)

CHAT_PERMISSIONS = DatasetItem(
    {
        "can_send_messages": True,
        "can_send_media_messages": True,
        "can_send_polls": True,
        "can_send_other_messages": True,
        "can_add_web_page_previews": True,
        "can_change_info": True,
        "can_invite_users": True,
        "can_pin_messages": True,
    },
    model=types.ChatPermissions,
)

CHAT_LOCATION = DatasetItem(
    {
        "location": LOCATION,
        "address": "address",
    },
    model=types.ChatLocation,
)
