from typing import List
from models.Account.StandardAccount import StandardAccount
from models.enums.AccountTypeEnum import AccountTypeEnum
from models.Transaction.GenericTransaction import GenericTransaction
from models.Account.GenericAccount import GenericAccount
from models.Transaction.DebitTransaction import DebitTransaction
from usecases.AccountValidator import validate_account_for_transaction
from usecases.TransactionValidator import validate_transaction_operation
from controllers.persistence.PersistenceController import get_db, EntityKeyEnum


def handle_transaction(transaction_operation: dict) -> dict:
    transaction = _convert_dict_to_transaction(transaction_operation)
    saved_account = _convert_dict_to_account(_get_account())
    transaction_history = _get_transaction_history()
    violations = _verify_transaction_violations(
        saved_account, transaction, transaction_history
    )
    validation_result = format_validation_result(violations, saved_account)
    if len(violations) == 0:
        _save_account_changes(saved_account, transaction)
    return validation_result


def _convert_dict_to_transaction(trans: dict) -> DebitTransaction:
    return DebitTransaction.from_dict(trans)


def _get_account() -> GenericAccount:
    return get_db().get_value(AccountTypeEnum.STANDARD_ACCOUNT.value)


def _convert_dict_to_account(acc: dict) -> StandardAccount:
    return StandardAccount.from_dict(acc)


def _save_account_changes(acc: GenericAccount, trans: GenericTransaction) -> None:
    acc.balance = acc.balance - trans.amount
    get_db().set_value(EntityKeyEnum.ACCOUNT_KEY.value, acc.to_dict())
    get_db().extend_value(EntityKeyEnum.TRANSACTION_HISTORY_KEY.value, trans.to_dict())


def _get_transaction_history() -> List[GenericTransaction]:
    transaction_history = get_db().get_value(
        EntityKeyEnum.TRANSACTION_HISTORY_KEY.value
    )
    return list(
        map(
            lambda it: _convert_dict_to_transaction(it),
            transaction_history if transaction_history else [],
        )
    )


def _verify_transaction_violations(
    acc: GenericAccount, trans: GenericTransaction, trans_hist: List[GenericTransaction]
) -> List[str]:
    violations = []
    violations.append(validate_account_for_transaction(acc is not None))
    violations.append(validate_transaction_operation(acc, trans, trans_hist))
    return violations


def format_validation_result(
    violation_list: List[str], account: GenericAccount
) -> List[dict]:
    validation_result = account.to_dict()
    validation_result["violations"] = violation_list
    return validation_result
