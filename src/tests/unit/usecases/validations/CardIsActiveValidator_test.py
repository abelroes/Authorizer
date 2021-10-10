from models.Account.StandardAccount import StandardAccount
from models.enums.AccountTypeEnum import AccountTypeEnum
from usecases.validations.CardIsActiveValidator import validate_card_is_active
from usecases.enums.ViolationEnum import ViolationEnum


def test_validate_card_is_active_returns_violation():
    account = StandardAccount(
        AccountTypeEnum.STANDARD_ACCOUNT,
        10,
        False
    )
    assert validate_card_is_active(
        account) == ViolationEnum.CARD_NOT_ACTIVE.value


def test_validate_card_is_active_returns_no_violation():
    account = StandardAccount(
        AccountTypeEnum.STANDARD_ACCOUNT,
        10,
        True
    )
    assert validate_card_is_active(account) == None


def test_validate_card_is_active_with_unexpected_value():
    account = StandardAccount(
        AccountTypeEnum.STANDARD_ACCOUNT,
        None,
        True
    )
    assert validate_card_is_active(account) == None
