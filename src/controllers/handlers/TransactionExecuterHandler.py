from typing import List, Set
from usecases.validations.AccountIsActiveValidator import validate_account_is_initialized
from usecases.Transaction.TransactionValidator import validate_transaction_operation
from controllers.formaters.SetFormater import remove_none_from_set
from models.Account.StandardAccount import StandardAccount
from models.enums.AccountTypeEnum import AccountTypeEnum
from models.Transaction.GenericTransaction import GenericTransaction
from models.Account.GenericAccount import GenericAccount
from models.Transaction.DebitTransaction import DebitTransaction
from controllers.persistence.PersistenceController import get_db, EntityKeyEnum


def handle_transaction(transaction_operation: dict) -> dict:
    transaction = _convert_dict_to_transaction(transaction_operation)
    saved_account = _convert_dict_to_account(_get_account())
    transaction_history = _get_transaction_history()
    violations = _verify_transaction_violations(
        saved_account, transaction, transaction_history
    )
    if len(remove_none_from_set(violations)) == 0:
        saved_account = _save_account_changes(saved_account, transaction)
    validation_result = format_validation_result(violations, saved_account)
    return validation_result


def _convert_dict_to_transaction(trans: dict) -> DebitTransaction:
    return DebitTransaction.from_dict(trans)


def _get_account() -> GenericAccount:
    return get_db().get_value(AccountTypeEnum.STANDARD_ACCOUNT.value)


def _convert_dict_to_account(acc: dict) -> StandardAccount:
    return StandardAccount.from_dict(acc) if acc else None


def _save_account_changes(
    acc: GenericAccount, trans: GenericTransaction
) -> GenericAccount:
    acc.change_balance(acc.balance - trans.amount)
    get_db().set_value(EntityKeyEnum.ACCOUNT_KEY.value, acc.to_dict())
    get_db().append_value_or_create(
        EntityKeyEnum.TRANSACTION_HISTORY_KEY.value, trans.to_dict()
    )
    return acc


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
    acc: GenericAccount, trans: GenericTransaction, trans_hist: Set[GenericTransaction]
) -> Set[str]:
    violations = {validate_account_is_initialized(acc is not None)}
    violations.update(validate_transaction_operation(acc, trans, trans_hist))
    return violations


def format_validation_result(violation_set: Set[str], account: GenericAccount) -> dict:
    validation_result = account.to_dict() if account else {"account": {}}
    validation_result["violations"] = list(remove_none_from_set(violation_set))
    return validation_result
