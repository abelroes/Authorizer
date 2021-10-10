import pytest
from models.Transaction.DebitTransaction import DebitTransaction
from models.enums.TransactionTypeEnum import TransactionTypeEnum
from usecases.validations.HasEnoughBalanceValidator import validate_account_has_balance
from models.Account.StandardAccount import StandardAccount
from models.enums.AccountTypeEnum import AccountTypeEnum
from usecases.enums.ViolationEnum import ViolationEnum
from models.formaters.DatetimeFormater import format_str_to_datetime


def test_validate_account_has_balance_returns_violation():
    account = StandardAccount(
        AccountTypeEnum.STANDARD_ACCOUNT,
        10,
        False
    )
    transaction = DebitTransaction(
        TransactionTypeEnum.DEBIT,
        20,
        format_str_to_datetime("2020-02-13T10:00:00.000Z"),
        'Lanchonete da Esquina'
    )
    assert validate_account_has_balance(
        account, transaction) == ViolationEnum.INSUFFICIENT_LIMIT.value


def test_validate_account_has_balance_returns_no_violation():
    account = StandardAccount(
        AccountTypeEnum.STANDARD_ACCOUNT,
        30,
        True
    )
    transaction = DebitTransaction(
        TransactionTypeEnum.DEBIT,
        20,
        format_str_to_datetime("2020-02-13T10:00:00.000Z"),
        'Lanchonete da Esquina'
    )
    assert validate_account_has_balance(account, transaction) == None


def test_validate_account_has_balance_with_unexpected_value():
    account = StandardAccount(
        AccountTypeEnum.STANDARD_ACCOUNT,
        None,
        True
    )
    transaction = DebitTransaction(
        TransactionTypeEnum.DEBIT,
        20,
        format_str_to_datetime("2020-02-13T10:00:00.000Z"),
        'Lanchonete da Esquina'
    )
    with pytest.raises(TypeError):
        validate_account_has_balance(account, transaction)
