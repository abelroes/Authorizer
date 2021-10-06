from typing import List
from NuTeste.src.usecases.enums.ViolationEnum import ViolationEnum
from models.Account.GenericAccount import GenericAccount


def validate_account_operation(
    account_already_existed: bool, account: GenericAccount
) -> List[str]:
    violations_list = []
    violations_list.append(_validate_account_should_exist(account_already_existed))
    return violations_list


def _validate_account_should_exist(account_already_existed: bool) -> List[str]:
    violations_list = []
    if account_already_existed:
        violations_list.append(ViolationEnum.ACCOUNT_ALREADY_EXISTS.value)
    return violations_list


def validate_account_for_transaction(account_already_existed: bool) -> List[str]:
    violations_list = []
    if not account_already_existed:
        violations_list.append(ViolationEnum.ACCOUNT_NOT_INITIALIZED.value)
    return violations_list
