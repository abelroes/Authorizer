from typing import List
from usecases.Transaction.TransactionValidationUtils import (
    has_doubled_last_transactions, has_transactions_in_last_2_minutes
)
from models.Transaction.GenericTransaction import GenericTransaction
from usecases.enums.ViolationEnum import ViolationEnum


def validate_transaction_duplication(
    trans: GenericTransaction, trans_hist: List[GenericTransaction]
) -> str:
    return (
        ViolationEnum.DOUBLED_TRANSACTION.value
        if len(trans_hist) > 0
        and has_doubled_last_transactions(trans, trans_hist)
        and has_transactions_in_last_2_minutes(trans, trans_hist)
        else None
    )
