from collections.abc import Mapping
from typing import Any


class DatasetItem(Mapping):
    def __init__(self, data: dict, *, model=None, name=None):
        self._data = data
        self._name = name
        self._model = model

    @property
    def data(self) -> dict:
        return self._data

    @property
    def name(self) -> str:
        return self._name

    @property
    def model(self) -> Any:
        return self._model

    def as_object(self, **replace_args) -> Any:
        """
        Build the model from the data; without a model return the data dict

        :return: Any
        """
        data = self._data.copy()
        data.update(**replace_args)
        self._drop_shadowing_aliases(data, replace_args)
        if self._model and isinstance(self._data, dict):
            return self._recursive_as_object(data, self._model)
        return data

    def _drop_shadowing_aliases(self, data: dict, replace_args: dict) -> None:
        """
        Data keeps some fields under their Telegram alias (``from``), so an override by the field name
        (``from_user``) would lose to the alias; drop the alias in that case
        """
        fields = getattr(self._model, "model_fields", {})
        for key in replace_args:
            field = fields.get(key)
            if field is not None and field.alias and field.alias != key:
                data.pop(field.alias, None)

    @classmethod
    def _recursive_as_object(cls, data: dict, model: Any):
        """
        Build the model from data, converting nested dataset items and lists of them first

        :param data: the dict that should be as object
        :param model: the object that will be returned
        :return:
        """
        converted = {key: cls._convert(value) for key, value in data.items()}
        return model(**converted)

    @classmethod
    def _convert(cls, value: Any) -> Any:
        if isinstance(value, DatasetItem):
            if value.model is None:
                return {key: cls._convert(item) for key, item in value.data.items()}
            return cls._recursive_as_object(value.data, value.model)
        if isinstance(value, list):
            return [cls._convert(item) for item in value]
        return value

    def __iter__(self):
        return iter(self._data.keys())

    def __getitem__(self, item):
        return self._data[item]

    def __len__(self):
        return len(self._data)
