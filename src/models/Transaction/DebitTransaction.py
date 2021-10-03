import GenericTransaction
from dataclasses import dataclass
from models.enums.TransactionTypeEnum import TransactionTypeEnum


@dataclass
class DebitTransaction(GenericTransaction):
    transaction_type = TransactionTypeEnum.DEBIT
    merchant: str