from usecases.validations.TransactionIsNotDuplicatedValidator import validate_transaction_duplication
from models.Transaction.DebitTransaction import DebitTransaction
from models.enums.TransactionTypeEnum import TransactionTypeEnum
from models.formaters.DatetimeFormater import format_str_to_datetime
from usecases.enums.ViolationEnum import ViolationEnum


def test_validate_transaction_duplication_returns_violation():
    transaction = DebitTransaction(
        TransactionTypeEnum.DEBIT,
        20,
        format_str_to_datetime("2020-02-13T10:01:00.000Z"),
        'Lanchonete da Esquina'
    )
    transaction_history = [
        DebitTransaction(TransactionTypeEnum.DEBIT, 20, format_str_to_datetime(
            "2020-02-13T10:00:00.000Z"), 'Lanchonete da Esquina'),
    ]
    assert validate_transaction_duplication(
        transaction, transaction_history) == ViolationEnum.DOUBLED_TRANSACTION.value


def test_validate_transaction_duplication_returns_violation_with_older_transactions():
    transaction = DebitTransaction(
        TransactionTypeEnum.DEBIT,
        20,
        format_str_to_datetime("2020-02-13T10:01:00.000Z"),
        'Lanchonete da Esquina'
    )
    transaction_history = [
        DebitTransaction(TransactionTypeEnum.DEBIT, 20, format_str_to_datetime(
            "2020-01-13T10:00:00.000Z"), 'Lanchonete da Esquina'),
    ]
    assert validate_transaction_duplication(
        transaction, transaction_history) == None


def test_validate_transaction_duplication_returns_no_violation_by_empty_list():
    transaction = DebitTransaction(
        TransactionTypeEnum.DEBIT,
        20,
        format_str_to_datetime("2020-02-13T10:00:00.000Z"),
        'Lanchonete da Esquina'
    )
    assert validate_transaction_duplication(transaction, []) == None


def test_validate_transaction_duplication_returns_no_violation_by_doubled_transaction():
    transaction = DebitTransaction(
        TransactionTypeEnum.DEBIT,
        20,
        format_str_to_datetime("2020-02-13T10:01:00.000Z"),
        'Lanchonete da Esquina'
    )
    transaction_history = [
        DebitTransaction(TransactionTypeEnum.DEBIT, 40, format_str_to_datetime(
            "2020-02-13T10:00:00.000Z"), 'Lanchonete da Outra Esquina'),
    ]
    assert validate_transaction_duplication(
        transaction, transaction_history) == None
