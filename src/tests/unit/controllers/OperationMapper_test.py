from controllers.OperationMapper import OperationMapper
from controllers.handlers.AccountCreatorHandler import handle_create_account
from controllers.handlers.TransactionExecuterHandler import handle_transaction


def test_operation_mapper_for_account_creation():
    expected_function = handle_create_account

    assert OperationMapper.from_operation_key('account') == expected_function


def test_operation_mapper_for_transaction():
    expected_function = handle_transaction

    assert OperationMapper.from_operation_key('transaction') == expected_function