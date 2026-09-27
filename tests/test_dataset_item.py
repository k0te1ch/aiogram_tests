import pytest
from aiogram import types

import aiogram_tests.types.dataset as dataset
from aiogram_tests.types.dataset import DatasetItem


def test_as_object():
    dataset_item = DatasetItem({"firstArg": 1, "secondArg": 2})
    assert dataset_item.as_object() == {"firstArg": 1, "secondArg": 2}
    assert dataset_item.as_object(firstArg=3) == {"firstArg": 3, "secondArg": 2}
    assert dataset_item.as_object(thirdArg=3) == {"firstArg": 1, "secondArg": 2, "thirdArg": 3}


def test_as_object_converting():
    dataset_item = DatasetItem(
        {
            "id": 12345678,
            "is_bot": False,
            "first_name": "FirstName",
            "last_name": "LastName",
            "username": "username",
        },
        model=types.User,
    )
    assert dataset_item.as_object() == types.User(
        id=12345678, is_bot=False, first_name="FirstName", last_name="LastName", username="username"
    )
    assert dataset_item.as_object(first_name="EditedFirstName") == types.User(
        id=12345678, is_bot=False, first_name="EditedFirstName", last_name="LastName", username="username"
    )
    assert dataset_item.as_object(language_code="ru") == types.User(
        id=12345678,
        is_bot=False,
        first_name="FirstName",
        last_name="LastName",
        username="username",
        language_code="ru",
    )


def test_as_object_converting_with_nesting():
    dataset_item = DatasetItem(
        {
            "message_id": 11223,
            "from": {
                "id": 12345678,
                "is_bot": False,
                "first_name": "FirstName",
                "last_name": "LastName",
                "username": "username",
            },
            "chat": {
                "id": 12345678,
                "first_name": "FirstName",
                "last_name": "LastName",
                "username": "username",
                "type": "private",
            },
            "date": 1508709711,
            "text": "Hi, world!",
        },
        model=types.Message,
    )
    assert dataset_item.as_object() == types.Message(
        message_id=11223,
        from_user=types.User(
            id=12345678, is_bot=False, first_name="FirstName", last_name="LastName", username="username"
        ),
        chat=types.Chat(id=12345678, first_name="FirstName", last_name="LastName", username="username", type="private"),
        date=1508709711,
        text="Hi, world!",
    )


def test_converting_all_dataset_items_to_model():
    all_items = (getattr(dataset, name) for name in dir(dataset))
    for item in all_items:
        if not isinstance(item, DatasetItem):
            continue

        item.as_object()


def test_override_by_field_name_wins_over_alias():
    message = dataset.MESSAGE.as_object(from_user=dataset.USER.as_object(id=42))

    assert message.from_user.id == 42


@pytest.mark.parametrize(
    "name",
    [name for name, item in vars(dataset).items() if isinstance(item, DatasetItem) and item.model is not None],
)
def test_dataset_item_builds_with_current_aiogram(name):
    # as_object() returns None when the model rejects the data, so a Bot API change shows up here
    assert getattr(dataset, name).as_object() is not None
