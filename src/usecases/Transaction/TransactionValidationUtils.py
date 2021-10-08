from functools import reduce
from datetime import datetime, timedelta
from typing import List
from models.Account.StandardAccount import StandardAccount
from models.Transaction.DebitTransaction import DebitTransaction
from models.Transaction.GenericTransaction import GenericTransaction


def positive_balance_after_transaction(
    acc: StandardAccount, trans: DebitTransaction
) -> bool:
    return (acc.balance - trans.amount) >= 0


def has_transactions_in_last_2_minutes(
    transaction: GenericTransaction, transactions: List[GenericTransaction]
) -> bool:
    diff_minutes = 2
    return reduce(
        lambda a, b: a and b,
        list(
            map(
                lambda it: time_difference_in_minutes(
                    transaction.time, it.time)
                <= timedelta(minutes=diff_minutes),
                transactions,
            )
        ),
    )


def has_doubled_last_transactions(
    transaction: GenericTransaction, transactions: List[GenericTransaction]
) -> bool:
    return reduce(
        lambda a, b: a or b,
        list(
            map(
                lambda it: compare_transactions(transaction, it),
                transactions,
            )
        ),
    )


def last_three_transactions(trans_hist: List[GenericTransaction]) -> List[str]:
    return trans_hist[-3: len(trans_hist)]


def time_difference_in_minutes(a: datetime, b: datetime) -> int:
    return abs(a - b)


def compare_transactions(a: GenericTransaction, b: GenericTransaction) -> bool:
    return a.merchant == b.merchant and a.amount == b.amount
