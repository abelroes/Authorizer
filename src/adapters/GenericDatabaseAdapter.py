from typing import Any


class GenericDatabaseAdapter:
    def __init__(self) -> None:
        pass

    def get_value(self, key: Any) -> Any:
        raise NotImplementedError

    def set_value(self, key: Any, value: Any) -> None:
        raise NotImplementedError

    def set_value_if_not_exists(self, key: Any, value: Any) -> bool:
        raise NotImplementedError

    def remove_key(self, key: Any) -> None:
        raise NotImplementedError