from datetime import datetime
from models.formaters.DatetimeFormater import (
    format_datetime_to_str,
    format_str_to_datetime,
)
from models.Transaction.GenericTransaction import GenericTransaction
from dataclasses import dataclass
from models.enums.TransactionTypeEnum import TransactionTypeEnum


@dataclass
class DebitTransaction(GenericTransaction):
    merchant: str

    @staticmethod
    def from_dict(data: dict):
        transaction_type = TransactionTypeEnum.DEBIT
        return DebitTransaction(
            transaction_type=transaction_type,
            amount=data[transaction_type.value]["amount"],
            time=format_str_to_datetime(data[transaction_type.value]["time"]),
            merchant=data[transaction_type.value]["merchant"],
        )

    def to_dict(self):
        return {
            self.transaction_type.value: {
                "merchant": self.merchant,
                "amount": self.amount,
                "time": format_datetime_to_str(self.time),
            }
        }
