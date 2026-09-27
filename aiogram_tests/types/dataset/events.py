"""Inline mode, polls, chat membership and reactions"""

from aiogram import types

from .base import DatasetItem
from .chats import CHAT
from .chats import USER

INLINE_QUERY = DatasetItem(
    {"id": "inline_query_id", "from": USER, "query": "search", "offset": ""},
    model=types.InlineQuery,
)

CHOSEN_INLINE_RESULT = DatasetItem(
    {"result_id": "result_id", "from": USER, "query": "search"},
    model=types.ChosenInlineResult,
)

# Newer Bot API versions add required poll fields; older aiogram keeps them as extra fields
POLL_OPTION = DatasetItem(
    {"persistent_id": "option_1", "text": "Yes", "voter_count": 1},
    model=types.PollOption,
)

POLL = DatasetItem(
    {
        "id": "poll_id",
        "question": "Is it working?",
        "options": [POLL_OPTION],
        "total_voter_count": 1,
        "is_closed": False,
        "is_anonymous": False,
        "type": "regular",
        "allows_multiple_answers": False,
        "allows_revoting": True,
        "members_only": False,
    },
    model=types.Poll,
)

POLL_ANSWER = DatasetItem(
    {"poll_id": "poll_id", "user": USER, "option_ids": [0], "option_persistent_ids": ["option_1"]},
    model=types.PollAnswer,
)

CHAT_MEMBER_MEMBER = DatasetItem({"user": USER, "status": "member"}, model=types.ChatMemberMember)

CHAT_MEMBER_LEFT = DatasetItem({"user": USER, "status": "left"}, model=types.ChatMemberLeft)

CHAT_MEMBER_UPDATED = DatasetItem(
    {
        "chat": CHAT,
        "from": USER,
        "date": 1508709711,
        "old_chat_member": CHAT_MEMBER_LEFT,
        "new_chat_member": CHAT_MEMBER_MEMBER,
    },
    model=types.ChatMemberUpdated,
)

CHAT_JOIN_REQUEST = DatasetItem(
    {"chat": CHAT, "from": USER, "user_chat_id": 12345678, "date": 1508709711},
    model=types.ChatJoinRequest,
)

REACTION_TYPE_EMOJI = DatasetItem({"type": "emoji", "emoji": "👍"}, model=types.ReactionTypeEmoji)

MESSAGE_REACTION_UPDATED = DatasetItem(
    {
        "chat": CHAT,
        "message_id": 11223,
        "user": USER,
        "date": 1508709711,
        "old_reaction": [],
        "new_reaction": [REACTION_TYPE_EMOJI],
    },
    model=types.MessageReactionUpdated,
)
