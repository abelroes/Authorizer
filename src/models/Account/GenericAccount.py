from dataclasses import dataclass
from models.enums.AccountTypeEnum import AccountTypeEnum


@dataclass
class GenericAccount:
    account_type: AccountTypeEnum
    balance: int

    @staticmethod
    def from_dict(data: dict):
        raise NotImplementedError

    def to_dict(self):
        raise NotImplementedError
