from typing import List
from models.Account.GenericAccount import GenericAccount


def validate_account_operation(account_already_existed: bool, account: GenericAccount) -> List[str]:
    violations_list = []
    if(account_already_existed): violations_list.append("account-already-initialized")
    return violations_list