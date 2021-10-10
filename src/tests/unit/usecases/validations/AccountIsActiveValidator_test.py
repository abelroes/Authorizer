from usecases.enums.ViolationEnum import ViolationEnum
from usecases.validations.AccountIsActiveValidator import validate_account_is_initialized


def test_validate_account_is_initialized_returns_violation():
    assert validate_account_is_initialized(
        False) == ViolationEnum.ACCOUNT_NOT_INITIALIZED.value


def test_validate_account_is_initialized_returns_no_violation():
    assert validate_account_is_initialized(True) == None


def test_validate_account_is_initialized_with_unexpected_value():
    assert validate_account_is_initialized(
        None) == ViolationEnum.ACCOUNT_NOT_INITIALIZED.value
