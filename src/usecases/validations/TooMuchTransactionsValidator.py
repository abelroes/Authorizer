from typing import List, Set
from usecases.Transaction.TransactionValidationUtils import has_transactions_in_last_2_minutes, last_three_transactions
from models.Transaction.GenericTransaction import GenericTransaction
from usecases.enums.ViolationEnum import ViolationEnum


def validate_transaction_frequency(
    trans: GenericTransaction, trans_hist: List[GenericTransaction]
) -> str:
    last_three_trans = last_three_transactions(trans_hist)
    return (
        ViolationEnum.HIGH_FREQUENCY.value
        if len(last_three_trans) >= 3
        and has_transactions_in_last_2_minutes(trans, last_three_trans)
        else None
    )
