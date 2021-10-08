from typing import Any, List
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
    
    def remove_key(self, key: Any) -> None:
        try:
            self.dictMap.pop(key)
        except(KeyError) as err:
            pass

    def append_value_or_create(self, key: Any, new_value: Any) -> None:
        saved_value: List = self.get_value(key)
        if saved_value is None:
            self.set_value(key, [new_value])
        else:
            saved_value.append(new_value)
            self.set_value(key, saved_value)
