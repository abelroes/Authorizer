from typing import Any
from decorators.singleton import singleton
from adapters.GenericDatabaseAdapter import GenericDatabaseAdapter


@singleton
class DictDBAdapter(GenericDatabaseAdapter):
    def __init__(self) -> None:
        self.dictMap = {}

    def get_value(self, key: Any) -> Any:
        return self.dictMap.get(key)

    def set_value(self, key: Any, value: Any) -> None:
        self.dictMap[key] = value

    def set_value_if_not_exists(self, key: Any, value: Any) -> bool:
        if self.get_value(key) is None:
            self.set_value(key, value)
            return True
        else:
            return False

    def append_value(self, key: Any, value: Any) -> None:
        self.set_value(key, self.get_value(key).append(value))
