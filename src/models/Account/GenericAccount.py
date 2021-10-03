from dataclasses import dataclass
from models.enums.AccountTypeEnum import AccountTypeEnum


@dataclass
class GenericAccount():
    account_type: AccountTypeEnum
    