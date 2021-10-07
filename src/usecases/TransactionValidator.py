from functools import reduce
from datetime import datetime
from typing import List
from models.Account.StandardAccount import StandardAccount
from models.Transaction.DebitTransaction import DebitTransaction
from usecases.enums.ViolationEnum import ViolationEnum
from models.Account.GenericAccount import GenericAccount
from models.Transaction.GenericTransaction import GenericTransaction


def validate_transaction_operation(
    account: GenericAccount,
    transaction: GenericTransaction,
    transaction_history: List[GenericTransaction],
) -> List[str]:
    violations_list = []
    violations_list.extend(_validate_card_active(account))
    violations_list.extend(_validate_account_limit(account, transaction))
    violations_list.extend(
        _validate_transaction_frequency(transaction, transaction_history)
        if len(transaction_history) > 0
        else []
    )
    return violations_list


def _validate_card_active(acc: StandardAccount) -> List[str]:
    return [ViolationEnum.CARD_NOT_ACTIVE.value] if not acc.card_status else []


def _validate_account_limit(acc: StandardAccount, trans: DebitTransaction) -> List[str]:
    return (
        [ViolationEnum.INSUFFICIENT_LIMIT.value]
        if not _positive_balance_after_transaction(acc, trans)
        else []
    )


def _validate_transaction_frequency(
    trans: GenericTransaction, trans_hist: List[GenericTransaction]
) -> List[str]:
    if _has_transactions_in_last_2_minutes(trans, trans_hist):
        return (
            [ViolationEnum.DOUBLE_TRANSACTION.value]
            if _has_last_transactions_doubled(trans, trans_hist)
            else [ViolationEnum.HIGH_FREQUENCY.value]
        )
    else:
        return []


def _positive_balance_after_transaction(
    acc: StandardAccount, trans: DebitTransaction
) -> bool:
    return (acc.balance - trans.amount) >= 0


def _has_transactions_in_last_2_minutes(
    trans: GenericTransaction, trans_hist: List[GenericTransaction]
) -> bool:
    diff_minutes = 2
    return reduce(
        lambda a, b: a and b,
        list(
            map(
                lambda it: _time_difference_in_minutes(trans.time, it.time)
                <= diff_minutes,
                _last_three_transactions(trans_hist),
            )
        ),
    )


def _has_last_transactions_doubled(
    trans: GenericTransaction, trans_hist: List[GenericTransaction]
) -> bool:
    return reduce(
        lambda a, b: a and b,
        list(
            map(
                lambda it: _compare_transactions(trans.time, it.time),
                _last_three_transactions(trans_hist),
            )
        ),
    )


def _last_three_transactions(trans_hist: List[GenericTransaction]) -> List[str]:
    return trans_hist[-3 : len(trans_hist)]


def _time_difference_in_minutes(a: datetime, b: datetime) -> int:
    return abs(a.min - b.min)


def _compare_transactions(a: GenericTransaction, b: GenericTransaction) -> bool:
    return a.merchant == b.merchant and a.amount == b.amount
