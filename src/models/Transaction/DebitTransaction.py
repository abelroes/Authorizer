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
            time=data[transaction_type.value]["time"],
            merchant=data[transaction_type.value]["merchant"],
        )

    def to_dict(self):
        return {
            self.transaction_type.value: {
                "merchant": self.merchant,
                "amount": self.amount,
                "time": self.time,
            }
        }
