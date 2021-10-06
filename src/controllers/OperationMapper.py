from enum import Enum
from dataclasses import dataclass
from typing import Callable, Any
from controllers.handlers.AccountCreatorHandler import handle_create_account
from controllers.handlers.TransactionExecuterHandler import handle_transaction


@dataclass
class Operation:
    operation: str
    runner: Callable[[Any], Any]


class OperationMapper(Enum):
    CREATE_ACCOUNT = Operation(operation="account", runner=handle_create_account)
    EXECUTE_TRANSACTION = Operation(operation="transaction", runner=handle_transaction)

    @classmethod
    def from_operation_key(cls, operation: str):
        return list(filter(lambda it: it.value.operation == operation, cls))[
            0
        ].value.runner
