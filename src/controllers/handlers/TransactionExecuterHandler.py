from typing import Set
from controllers.handlers.AccountCreatorHandler import convert_dict_to_account
from controllers.handlers.HandlerUtils import (
    convert_dict_to_transaction, format_validation_result,
    get_saved_account, get_transaction_history, save_account_changes
)
from usecases.validations.AccountIsActiveValidator import validate_account_is_initialized
from usecases.Transaction.TransactionValidator import validate_transaction_operation
from controllers.formaters.SetFormater import remove_none_from_set
from models.Transaction.GenericTransaction import GenericTransaction
from models.Account.GenericAccount import GenericAccount


def handle_transaction(transaction_operation: dict) -> dict:
    saved_account = convert_dict_to_account(get_saved_account())
    transaction = convert_dict_to_transaction(transaction_operation)
    violations = _verify_transaction_violations(
        acc=saved_account,
        trans=transaction,
        trans_hist=get_transaction_history()
    )
    if len(remove_none_from_set(violations)) == 0:
        saved_account = save_account_changes(saved_account, transaction)
    validation_result = format_validation_result(violations, saved_account)
    return validation_result


def _verify_transaction_violations(
    acc: GenericAccount, trans: GenericTransaction, trans_hist: Set[GenericTransaction]
) -> Set[str]:
    violations = {validate_account_is_initialized(acc is not None)}
    violations.update(validate_transaction_operation(acc, trans, trans_hist))
    return violations
