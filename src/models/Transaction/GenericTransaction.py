import datetime
from dataclasses import dataclass
from models.enums.TransactionTypeEnum import TransactionTypeEnum


@dataclass
class GenericTransaction():
    transaction_type: TransactionTypeEnum
    amount: int
    time: datetime