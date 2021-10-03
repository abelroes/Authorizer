from dataclasses import dataclass
import GenericAccount
from models.enums.AccountTypeEnum import AccountTypeEnum


@dataclass
class StandardAccount(GenericAccount):
    account_type = AccountTypeEnum.STANDARD_ACCOUNT
    card_status: bool = False
    available_limit: int = 0