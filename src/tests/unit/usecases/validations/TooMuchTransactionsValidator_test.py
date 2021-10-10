from models.Transaction.DebitTransaction import DebitTransaction
from models.enums.TransactionTypeEnum import TransactionTypeEnum
from models.formaters.DatetimeFormater import format_str_to_datetime
from usecases.validations.TooMuchTransactionsValidator import validate_transaction_frequency
from usecases.enums.ViolationEnum import ViolationEnum


def test_validate_transaction_frequency_returns_violation():
    transaction = DebitTransaction(
        TransactionTypeEnum.DEBIT,
        40,
        format_str_to_datetime("2020-02-13T10:01:00.000Z"),
        'Lanchonete da Esquina'
    )
    transaction_history = [
        DebitTransaction(TransactionTypeEnum.DEBIT, 10, format_str_to_datetime(
            "2020-02-13T10:00:50.000Z"), 'Lanchonete da Esquina'),
        DebitTransaction(TransactionTypeEnum.DEBIT, 20, format_str_to_datetime(
            "2020-02-13T10:00:20.000Z"), 'PF do João'),
        DebitTransaction(TransactionTypeEnum.DEBIT, 30, format_str_to_datetime(
            "2020-02-13T10:00:00.000Z"), 'Restaurante Chic'),
    ]
    assert validate_transaction_frequency(
        transaction, transaction_history) == ViolationEnum.HIGH_FREQUENCY.value


def test_validate_transaction_frequency_returns_violation_with_older_transaction():
    transaction = DebitTransaction(
        TransactionTypeEnum.DEBIT,
        40,
        format_str_to_datetime("2020-02-13T10:01:00.000Z"),
        'Lanchonete da Esquina'
    )
    transaction_history = [
        DebitTransaction(TransactionTypeEnum.DEBIT, 50, format_str_to_datetime(
            "2020-02-13T09:00:00.000Z"), 'Lanchonete da Outra Esquina'),
        DebitTransaction(TransactionTypeEnum.DEBIT, 30, format_str_to_datetime(
            "2020-02-13T10:00:00.000Z"), 'Restaurante Chic'),
        DebitTransaction(TransactionTypeEnum.DEBIT, 20, format_str_to_datetime(
            "2020-02-13T10:00:20.000Z"), 'PF do João'),
        DebitTransaction(TransactionTypeEnum.DEBIT, 10, format_str_to_datetime(
            "2020-02-13T10:00:50.000Z"), 'Lanchonete da Esquina'),
    ]
    assert validate_transaction_frequency(
        transaction, transaction_history) == ViolationEnum.HIGH_FREQUENCY.value


def test_validate_transaction_frequency_returns_no_violation_with_out_of_order_history():
    transaction = DebitTransaction(
        TransactionTypeEnum.DEBIT,
        40,
        format_str_to_datetime("2020-02-13T10:01:00.000Z"),
        'Lanchonete da Esquina'
    )
    transaction_history = [
        DebitTransaction(TransactionTypeEnum.DEBIT, 10, format_str_to_datetime(
            "2020-02-13T10:00:50.000Z"), 'Lanchonete da Esquina'),
        DebitTransaction(TransactionTypeEnum.DEBIT, 20, format_str_to_datetime(
            "2020-02-13T10:00:20.000Z"), 'PF do João'),
        DebitTransaction(TransactionTypeEnum.DEBIT, 30, format_str_to_datetime(
            "2020-02-13T10:00:00.000Z"), 'Restaurante Chic'),
        DebitTransaction(TransactionTypeEnum.DEBIT, 50, format_str_to_datetime(
            "2020-02-13T09:00:00.000Z"), 'Lanchonete da Outra Esquina'),
    ]
    assert validate_transaction_frequency(
        transaction, transaction_history) == None


def test_validate_transaction_frequency_returns_no_violation_by_short_list():
    transaction = DebitTransaction(
        TransactionTypeEnum.DEBIT,
        20,
        format_str_to_datetime("2020-02-13T10:00:00.000Z"),
        'Lanchonete da Esquina'
    )
    transaction_history = [
        DebitTransaction(TransactionTypeEnum.DEBIT, 10, format_str_to_datetime(
            "2020-02-13T10:00:50.000Z"), 'Lanchonete da Esquina'),
        DebitTransaction(TransactionTypeEnum.DEBIT, 20, format_str_to_datetime(
            "2020-02-13T10:00:20.000Z"), 'PF do João'),
    ]
    assert validate_transaction_frequency(
        transaction, transaction_history) == None


def test_validate_transaction_frequency_returns_no_violation_by_empty_list():
    transaction = DebitTransaction(
        TransactionTypeEnum.DEBIT,
        20,
        format_str_to_datetime("2020-02-13T10:00:00.000Z"),
        'Lanchonete da Esquina'
    )
    assert validate_transaction_frequency(transaction, []) == None


def test_validate_transaction_frequency_returns_no_violation_by_old_transactions():
    transaction = DebitTransaction(
        TransactionTypeEnum.DEBIT,
        20,
        format_str_to_datetime("2020-02-13T10:50:00.000Z"),
        'Lanchonete da Esquina'
    )
    transaction_history = [
        DebitTransaction(TransactionTypeEnum.DEBIT, 10, format_str_to_datetime(
            "1992-05-09T10:00:50.000Z"), 'Lanchonete da Esquina'),
        DebitTransaction(TransactionTypeEnum.DEBIT, 20, format_str_to_datetime(
            "1992-05-09T10:00:20.000Z"), 'PF do João'),
        DebitTransaction(TransactionTypeEnum.DEBIT, 30, format_str_to_datetime(
            "1992-05-09T10:00:00.000Z"), 'Restaurante Chic'),
    ]
    assert validate_transaction_frequency(
        transaction, transaction_history) == None
