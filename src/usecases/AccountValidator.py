from typing import List
from usecases.enums.ViolationEnum import ViolationEnum
from models.Account.GenericAccount import GenericAccount


def validate_account_operation(
    account_already_existed: bool, account: GenericAccount
) -> List[str]:
    violations_list = []
    violations_list.extend(_validate_account_should_exist(account_already_existed))
    return violations_list


def _validate_account_should_exist(account_already_existed: bool) -> List[str]:
    return [ViolationEnum.ACCOUNT_ALREADY_EXISTS.value] if account_already_existed else []


def validate_account_for_transaction(account_already_existed: bool) -> List[str]:
    return [ViolationEnum.ACCOUNT_NOT_INITIALIZED.value] if not account_already_existed else []
