from typing import List, Set
from controllers.formaters.SetFormater import remove_none_from_set
from models.Account.StandardAccount import StandardAccount
from models.enums.AccountTypeEnum import AccountTypeEnum
from models.Transaction.GenericTransaction import GenericTransaction
from models.Account.GenericAccount import GenericAccount
from models.Transaction.DebitTransaction import DebitTransaction
from controllers.persistence.PersistenceController import get_db, EntityKeyEnum


def is_account_already_exists(account: StandardAccount) -> bool:
    return not get_db().set_value_if_not_exists(
        EntityKeyEnum.ACCOUNT_KEY.value, account.to_dict()
    )


def convert_dict_to_account(acc: dict) -> StandardAccount:
    return StandardAccount.from_dict(acc) if acc else None


def convert_dict_to_transaction(trans: dict) -> DebitTransaction:
    return DebitTransaction.from_dict(trans)


def format_validation_result(violation_set: Set[str], account: GenericAccount) -> dict:
    validation_result = account.to_dict() if account else {"account": {}}
    validation_result["violations"] = list(remove_none_from_set(violation_set))
    return validation_result


def get_saved_account() -> GenericAccount:
    return get_db().get_value(AccountTypeEnum.STANDARD_ACCOUNT.value)


def get_transaction_history() -> List[GenericTransaction]:
    transaction_history = get_db().get_value(
        EntityKeyEnum.TRANSACTION_HISTORY_KEY.value
    )
    return list(
        map(
            lambda it: convert_dict_to_transaction(it),
            transaction_history if transaction_history else [],
        )
    )


def save_account_changes(
    acc: GenericAccount, trans: GenericTransaction
) -> GenericAccount:
    acc.change_balance(acc.balance - trans.amount)
    get_db().set_value(EntityKeyEnum.ACCOUNT_KEY.value, acc.to_dict())
    get_db().append_value_or_create(
        EntityKeyEnum.TRANSACTION_HISTORY_KEY.value, trans.to_dict()
    )
    return acc
