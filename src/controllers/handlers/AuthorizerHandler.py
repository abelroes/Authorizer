from typing import List
from controllers.OperationMapper import OperationMapper


def handle_input(input_list: List[dict]) -> List[dict]:
    return list(map(lambda operation: authorize_operation(operation), input_list))


def authorize_operation(operation: dict) -> dict:
    authorize = OperationMapper.from_operation_key(list(operation.keys())[0])
    return authorize(operation)
