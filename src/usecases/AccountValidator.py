from typing import Set
from usecases.enums.ViolationEnum import ViolationEnum
from models.Account.GenericAccount import GenericAccount


def validate_account_operation(
    account_already_existed: bool, account: GenericAccount
) -> Set[str]:
    return {_validate_account_should_exist(account_already_existed)}


def _validate_account_should_exist(account_already_existed: bool) -> str:
    return (
        ViolationEnum.ACCOUNT_ALREADY_EXISTS.value if account_already_existed else None
    )


def validate_account_for_transaction(account_already_existed: bool) -> str:
    return (
        ViolationEnum.ACCOUNT_NOT_INITIALIZED.value
        if not account_already_existed
        else None
    )
