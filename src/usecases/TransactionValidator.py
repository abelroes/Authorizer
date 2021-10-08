from functools import reduce
from datetime import datetime, timedelta
from typing import List, Set
from models.Account.StandardAccount import StandardAccount
from models.Transaction.DebitTransaction import DebitTransaction
from usecases.enums.ViolationEnum import ViolationEnum
from models.Account.GenericAccount import GenericAccount
from models.Transaction.GenericTransaction import GenericTransaction


def validate_transaction_operation(
    account: GenericAccount,
    transaction: GenericTransaction,
    transaction_history: List[GenericTransaction],
) -> Set[str]:
    return {
        _validate_card_active(account),
        _validate_account_limit(account, transaction),
        _validate_transaction_frequency(transaction, transaction_history),
        _validate_transaction_duplication(transaction, transaction_history),
    }


def _validate_card_active(acc: StandardAccount) -> str:
    if acc:
        return ViolationEnum.CARD_NOT_ACTIVE.value if not acc.card_status else None
    else:
        return None


def _validate_account_limit(acc: StandardAccount, trans: DebitTransaction) -> str:
    if acc:
        return (
            ViolationEnum.INSUFFICIENT_LIMIT.value
            if not _positive_balance_after_transaction(acc, trans)
            else None
        )
    else:
        return None


def _validate_transaction_frequency(
    trans: GenericTransaction, trans_hist: List[GenericTransaction]
) -> str:
    last_three_trans = _last_three_transactions(trans_hist)
    return (
        ViolationEnum.HIGH_FREQUENCY.value
        if len(last_three_trans) >= 3
        and _has_transactions_in_last_2_minutes(trans, last_three_trans)
        else None
    )


def _validate_transaction_duplication(
    trans: GenericTransaction, trans_hist: List[GenericTransaction]
) -> str:
    return (
        ViolationEnum.DOUBLE_TRANSACTION.value
        if len(trans_hist) > 0
        and _has_last_transactions_doubled(trans, trans_hist)
        and _has_transactions_in_last_2_minutes(trans, trans_hist)
        else None
    )


def _positive_balance_after_transaction(
    acc: StandardAccount, trans: DebitTransaction
) -> bool:
    return (acc.balance - trans.amount) >= 0


def _has_transactions_in_last_2_minutes(
    transaction: GenericTransaction, transactions: List[GenericTransaction]
) -> bool:
    diff_minutes = 2
    return reduce(
        lambda a, b: a and b,
        list(
            map(
                lambda it: _time_difference_in_minutes(transaction.time, it.time)
                <= timedelta(minutes=diff_minutes),
                transactions,
            )
        ),
    )


def _has_last_transactions_doubled(
    transaction: GenericTransaction, transactions: List[GenericTransaction]
) -> bool:
    return reduce(
        lambda a, b: a or b,
        list(
            map(
                lambda it: _compare_transactions(transaction, it),
                transactions,
            )
        ),
    )


def _last_three_transactions(trans_hist: List[GenericTransaction]) -> List[str]:
    return trans_hist[-3 : len(trans_hist)]


def _time_difference_in_minutes(a: datetime, b: datetime) -> int:
    return abs(a - b)


def _compare_transactions(a: GenericTransaction, b: GenericTransaction) -> bool:
    return a.merchant == b.merchant and a.amount == b.amount
