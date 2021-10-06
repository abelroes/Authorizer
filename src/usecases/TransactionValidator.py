from typing import List
from NuTeste.src.models.Account.StandardAccount import StandardAccount
from NuTeste.src.models.Transaction.DebitTransaction import DebitTransaction
from usecases.enums.ViolationEnum import ViolationEnum
from models.Account.GenericAccount import GenericAccount
from models.Transaction.GenericTransaction import GenericTransaction


def validate_transaction_operation(
    account: GenericAccount,
    transaction: GenericTransaction,
    transaction_history: List[GenericTransaction],
) -> List[str]:
    violations_list = []
    violations_list.append(_validate_card_active(account))
    violations_list.append(_validate_account_limit(account, transaction))
    violations_list.append(
        _validate_transaction_frequency(account, transaction, transaction_history)
    )
    violations_list.append(
        _validate_double_transaction(account, transaction, transaction_history)
    )
    return violations_list


def _validate_card_active(acc: StandardAccount) -> List[str]:
    violations_list = []
    if acc.card_status:
        violations_list.append(ViolationEnum.CARD_NOT_ACTIVE.value)
    return violations_list


def _validate_account_limit(acc: StandardAccount, trans: DebitTransaction) -> List[str]:
    violations_list = []
    if not _check_balance_after_transaction(acc, trans):
        violations_list.append(ViolationEnum.INSUFFICIENT_LIMIT.value)
    return violations_list


def _validate_transaction_frequency(
    acc: GenericAccount, trans: GenericTransaction, trans_hist: List[GenericTransaction]
) -> List[str]:
    violations_list = []
    if acc.card_status:
        violations_list.append(ViolationEnum.HIGH_FREQUENCY.value)
    return violations_list


def _validate_double_transaction(
    acc: GenericAccount, trans: GenericTransaction, trans_hist: List[GenericTransaction]
) -> List[str]:
    violations_list = []
    if acc.card_status:
        violations_list.append(ViolationEnum.DOUBLE_TRANSACTION.value)
    return violations_list


def _check_balance_after_transaction(
    acc: StandardAccount, trans: DebitTransaction
) -> bool:
    return (acc.balance - trans.amount) >= 0
