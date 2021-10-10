from usecases.enums.ViolationEnum import ViolationEnum
from usecases.Account.AccountValidator import validate_account_operation


def test_validate_account_operation_existing_account():
    assert validate_account_operation(True) == {ViolationEnum.ACCOUNT_ALREADY_EXISTS.value}

def test_validate_account_operation_not_existing_account():
    assert validate_account_operation(False) == {None}
