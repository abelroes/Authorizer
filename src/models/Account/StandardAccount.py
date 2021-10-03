from dataclasses import dataclass
from models.Account.GenericAccount import GenericAccount
from models.enums.AccountTypeEnum import AccountTypeEnum


@dataclass
class StandardAccount(GenericAccount):
    card_status: bool

    @staticmethod
    def from_dict(data: dict):
        return StandardAccount(
            account_type=AccountTypeEnum.STANDARD_ACCOUNT,
            balance=data["account"]["available-limit"],
            card_status=data["account"]["active-card"],
        )

    def to_dict(self):
        return {
            self.account_type.value: {
                "active-card": self.card_status,
                "available-limit": self.balance,
            }
        }
