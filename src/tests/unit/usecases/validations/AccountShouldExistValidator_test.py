from usecases.validations.AccountShouldExistValidator import validate_account_should_exist
from usecases.enums.ViolationEnum import ViolationEnum


def test_validate_account_should_exist_returns_violation():
    assert validate_account_should_exist(
        True) == ViolationEnum.ACCOUNT_ALREADY_EXISTS.value


def test_validate_account_should_exist_returns_no_violation():
    assert validate_account_should_exist(False) == None


def test_validate_account_should_exist_with_unexpected_value():
    assert validate_account_should_exist(None) == None
