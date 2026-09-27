"""Files and media attachments"""

from aiogram import types

from .base import DatasetItem

PHOTO = DatasetItem(
    {
        "file_id": "AgADBAADFak0G88YZAf8OAug7bHyS9x2ZxkABHVfpJywcloRAAGAAQABAg",
        "file_unique_id": "file_unique_id",
        "file_size": 1101,
        "width": 90,
        "height": 51,
    },
    model=types.PhotoSize,
)

AUDIO = DatasetItem(
    {
        "duration": 236,
        "mime_type": "audio/mpeg3",
        "title": "The Best Song",
        "performer": "The Best Singer",
        "file_id": "CQADAgADbQEAAsnrIUpNoRRNsH7_hAI",
        "file_size": 9507774,
        "file_unique_id": "file_unique_id",
    },
    model=types.Audio,
)

CONTACT = DatasetItem(
    {
        "phone_number": "88005553535",
        "first_name": "John",
        "last_name": "Smith",
    },
    model=types.Contact,
)

DICE = DatasetItem({"value": 6, "emoji": "🎲"}, model=types.Dice)

DOCUMENT = DatasetItem(
    {
        "file_name": "test.docx",
        "mime_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "file_id": "BQADAgADpgADy_JxS66XQTBRHFleAg",
        "file_unique_id": "file_unique_id",
        "file_size": 21331,
    },
    model=types.Document,
)

ANIMATION = DatasetItem(
    {"file_id": "file_id", "file_unique_id": "file_unique_id", "width": 50, "height": 50, "duration": 50},
    model=types.Animation,
)

GAME = DatasetItem(
    {
        "title": "Karate Kido",
        "description": "No trees were harmed in the making of this game :)",
        "photo": [PHOTO, PHOTO, PHOTO],
        "animation": ANIMATION,
    },
    model=types.Game,
)

LOCATION = DatasetItem(
    {
        "latitude": 50.693416,
        "longitude": 30.624605,
    },
    model=types.Location,
)

VENUE = DatasetItem(
    {
        "location": LOCATION,
        "title": "Venue Name",
        "address": "Venue Address",
        "foursquare_id": "4e6f2cec483bad563d150f98",
    },
    model=types.Venue,
)

STICKER = DatasetItem(
    {
        "width": 512,
        "height": 512,
        "emoji": "🛠",
        "set_name": "StickerSet",
        "thumb": PHOTO,
        "file_id": "AAbbCCddEEffGGhh1234567890",
        "file_size": 12345,
        "file_unique_id": "file_unique_id",
        "type": "type",
        "is_animated": False,
        "is_video": False,
    },
    model=types.Sticker,
)

VIDEO = DatasetItem(
    {
        "duration": 52,
        "width": 853,
        "height": 480,
        "mime_type": "video/quicktime",
        "thumb": PHOTO,
        "file_id": "BAADAgpAADdawy_JxS72kRvV3cortAg",
        "file_unique_id": "file_unique_id",
        "file_size": 10099782,
    },
    model=types.Video,
)

VIDEO_NOTE = DatasetItem(
    {
        "duration": 4,
        "length": 240,
        "thumb": PHOTO,
        "file_id": "AbCdEfGhIjKlMnOpQrStUvWxYz",
        "file_unique_id": "file_unique_id",
        "file_size": 186562,
    },
    model=types.VideoNote,
)

VOICE = DatasetItem(
    {
        "duration": 1,
        "mime_type": "audio/ogg",
        "file_id": "AwADawAgADADy_JxS2gopIVIIxlhAg",
        "file_unique_id": "file_unique_id",
        "file_size": 4321,
    },
    model=types.Voice,
)

FILE = DatasetItem(
    {"file_id": "XXXYYYZZZ", "file_size": 5254, "file_path": "voice/file_8", "file_unique_id": "file_unique_id"},
    model=types.File,
)
