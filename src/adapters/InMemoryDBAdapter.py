from typing import Any
from decorators.singleton import singleton

@singleton
class InMemoryDBAdapter:
    def __init__(self) -> None:
        self.memoryMap = {}
    
    def get_value(self, key: Any) -> Any:
        return self.memoryMap.get(key)
    
    def set_value(self, key: Any, value: Any) -> None:
        self.memoryMap[key] = value
    
    def set_value_if_not_exists(self, key: Any, value: Any) -> bool:
        if(self.get_value(key) is None):
            self.set_value(key, value)
            return True
        else:
            return False