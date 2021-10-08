from typing import Any, Set


def remove_none_from_set(s: Set[Any]) -> Set[Any]:
    return s - {None}
