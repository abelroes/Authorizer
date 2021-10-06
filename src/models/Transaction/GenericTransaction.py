import datetime
from dataclasses import dataclass
from models.enums.TransactionTypeEnum import TransactionTypeEnum


@dataclass
class GenericTransaction:
    transaction_type: TransactionTypeEnum
    amount: int
    time: datetime

    @staticmethod
    def from_dict(data: dict):
        raise NotImplementedError

    def to_dict(self):
        raise NotImplementedError
