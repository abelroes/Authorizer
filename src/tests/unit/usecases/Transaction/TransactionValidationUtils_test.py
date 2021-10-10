import pytest
from datetime import timedelta
from models.Account.StandardAccount import StandardAccount
from models.Transaction.DebitTransaction import DebitTransaction
from models.enums.AccountTypeEnum import AccountTypeEnum
from models.enums.TransactionTypeEnum import TransactionTypeEnum
from models.formaters.DatetimeFormater import format_str_to_datetime
from usecases.Transaction.TransactionValidationUtils import (
    compare_transactions, has_doubled_last_transactions,
    last_three_transactions, positive_balance_after_transaction,
    time_difference_in_minutes, has_transactions_in_last_2_minutes
)


def test_positive_balance_after_transaction_positive_balance():
    assert positive_balance_after_transaction(
        StandardAccount(
            AccountTypeEnum.STANDARD_ACCOUNT,
            20,
            True
        ),
        DebitTransaction(
            TransactionTypeEnum.DEBIT,
            10,
            format_str_to_datetime("2020-02-13T10:00:00.000Z"),
            'Lanchonete da Esquina'
        )
    )


def test_positive_balance_after_transaction_negative_balance():
    assert not positive_balance_after_transaction(
        StandardAccount(
            AccountTypeEnum.STANDARD_ACCOUNT,
            10,
            True
        ),
        DebitTransaction(
            TransactionTypeEnum.DEBIT,
            20,
            format_str_to_datetime("2020-02-13T10:00:00.000Z"),
            'Lanchonete da Esquina'
        )
    )


def test_positive_balance_after_transaction_invalid_account_value():
    with pytest.raises(TypeError):
        positive_balance_after_transaction(
            StandardAccount(
                AccountTypeEnum.STANDARD_ACCOUNT,
                None,
                True
            ),
            DebitTransaction(
                TransactionTypeEnum.DEBIT,
                20,
                format_str_to_datetime("2020-02-13T10:00:00.000Z"),
                'Lanchonete da Esquina'
            )
        )


def test_positive_balance_after_transaction_invalid_transaction_value():
    with pytest.raises(TypeError):
        positive_balance_after_transaction(
            StandardAccount(
                AccountTypeEnum.STANDARD_ACCOUNT,
                20,
                True
            ),
            DebitTransaction(
                TransactionTypeEnum.DEBIT,
                None,
                format_str_to_datetime("2020-02-13T10:00:00.000Z"),
                'Lanchonete da Esquina'
            )
        )


def test_has_transactions_in_last_2_minutes_returns_true():
    assert has_transactions_in_last_2_minutes(
        DebitTransaction(
            TransactionTypeEnum.DEBIT,
            20,
            format_str_to_datetime("2020-02-13T10:01:00.000Z"),
            'Lanchonete da Esquina'
        ),
        [
            DebitTransaction(TransactionTypeEnum.DEBIT, 10, format_str_to_datetime(
                "2020-02-13T10:00:00.000Z"), 'Lanchonete da Esquina'),
        ]
    )


def test_has_transactions_in_last_2_minutes_returns_false():
    assert not has_transactions_in_last_2_minutes(
        DebitTransaction(
            TransactionTypeEnum.DEBIT,
            20,
            format_str_to_datetime("2020-02-13T11:00:00.000Z"),
            'Lanchonete da Esquina'
        ),
        [
            DebitTransaction(TransactionTypeEnum.DEBIT, 10, format_str_to_datetime(
                "2020-02-13T10:00:00.000Z"), 'Lanchonete da Esquina'),
        ]
    )


def test_has_transactions_in_last_2_minutes_returns_false_in_limit_value():
    assert not has_transactions_in_last_2_minutes(
        DebitTransaction(
            TransactionTypeEnum.DEBIT,
            20,
            format_str_to_datetime("2020-02-13T10:02:00.001Z"),
            'Lanchonete da Esquina'
        ),
        [
            DebitTransaction(TransactionTypeEnum.DEBIT, 10, format_str_to_datetime(
                "2020-02-13T10:00:00.000Z"), 'Lanchonete da Esquina'),
        ]
    )


def test_has_transactions_in_last_2_minutes_returns_true_in_limit_value_1():
    assert has_transactions_in_last_2_minutes(
        DebitTransaction(
            TransactionTypeEnum.DEBIT,
            20,
            format_str_to_datetime("2020-02-13T10:00:00.001Z"),
            'Lanchonete da Esquina'
        ),
        [
            DebitTransaction(TransactionTypeEnum.DEBIT, 10, format_str_to_datetime(
                "2020-02-13T10:00:00.000Z"), 'Lanchonete da Esquina'),
        ]
    )


def test_has_transactions_in_last_2_minutes_returns_true_in_limit_value_2():
    assert has_transactions_in_last_2_minutes(
        DebitTransaction(
            TransactionTypeEnum.DEBIT,
            20,
            format_str_to_datetime("2020-02-13T10:01:59.999Z"),
            'Lanchonete da Esquina'
        ),
        [
            DebitTransaction(TransactionTypeEnum.DEBIT, 10, format_str_to_datetime(
                "2020-02-13T10:00:00.000Z"), 'Lanchonete da Esquina'),
        ]
    )


def test_has_doubled_last_transactions_returns_true():
    assert has_doubled_last_transactions(
        DebitTransaction(
            TransactionTypeEnum.DEBIT,
            20,
            format_str_to_datetime("2020-02-13T10:00:00.000Z"),
            'Lanchonete da Esquina'
        ),
        [
            DebitTransaction(TransactionTypeEnum.DEBIT, 20, format_str_to_datetime(
                "2020-02-13T10:01:59.999Z"), 'Lanchonete da Esquina'),
        ]
    )


def test_has_doubled_last_transactions_returns_false_by_name():
    assert not has_doubled_last_transactions(
        DebitTransaction(
            TransactionTypeEnum.DEBIT,
            20,
            format_str_to_datetime("2020-02-13T10:00:00.000Z"),
            'Lanchonete da Esquina'
        ),
        [
            DebitTransaction(TransactionTypeEnum.DEBIT, 20, format_str_to_datetime(
                "2020-02-13T10:01:59.999Z"), 'Lanchonete da Outra Esquina'),
        ]
    )


def test_has_doubled_last_transactions_returns_false_by_value():
    assert not has_doubled_last_transactions(
        DebitTransaction(
            TransactionTypeEnum.DEBIT,
            2,
            format_str_to_datetime("2020-02-13T10:00:00.000Z"),
            'Lanchonete da Esquina'
        ),
        [
            DebitTransaction(TransactionTypeEnum.DEBIT, 20, format_str_to_datetime(
                "2020-02-13T10:01:59.999Z"), 'Lanchonete da Esquina'),
        ]
    )


def test_last_three_transactions_gets_no_transaction():
    assert last_three_transactions([]) == []


def test_last_three_transactions_gets_one_transaction():
    assert len(last_three_transactions(
        [
            DebitTransaction(TransactionTypeEnum.DEBIT, 20, format_str_to_datetime(
                "2020-02-13T10:01:59.999Z"), 'Lanchonete da Esquina'),
        ]
    )) == 1


def test_last_three_transactions_gets_two_transactions():
    assert len(last_three_transactions(
        [
            DebitTransaction(TransactionTypeEnum.DEBIT, 10, format_str_to_datetime(
                "2020-02-13T10:00:00.000Z"), 'Lanchonete da Esquina'),
            DebitTransaction(TransactionTypeEnum.DEBIT, 10, format_str_to_datetime(
                "2020-02-13T11:00:00.000Z"), 'PF do João'),
        ]
    )) == 2


def test_last_three_transactions_gets_three_transactions():
    assert len(last_three_transactions(
        [
            DebitTransaction(TransactionTypeEnum.DEBIT, 10, format_str_to_datetime(
                "2020-02-13T10:00:00.000Z"), 'Lanchonete da Esquina'),
            DebitTransaction(TransactionTypeEnum.DEBIT, 10, format_str_to_datetime(
                "2020-02-13T11:00:00.000Z"), 'PF do João'),
            DebitTransaction(TransactionTypeEnum.DEBIT, 1000, format_str_to_datetime(
                "2020-02-13T21:00:00.000Z"), 'Restaurante Chic'),
        ]
    )) == 3


def test_last_three_transactions_gets_three_transactions_even_with_4_transactions():
    assert len(last_three_transactions(
        [
            DebitTransaction(TransactionTypeEnum.DEBIT, 10, format_str_to_datetime(
                "2020-02-13T10:00:00.000Z"), 'Lanchonete da Esquina'),
            DebitTransaction(TransactionTypeEnum.DEBIT, 10, format_str_to_datetime(
                "2020-02-13T11:00:00.000Z"), 'PF do João'),
            DebitTransaction(TransactionTypeEnum.DEBIT, 1000, format_str_to_datetime(
                "2020-02-13T21:00:00.000Z"), 'Restaurante Chic'),
            DebitTransaction(TransactionTypeEnum.DEBIT, 10, format_str_to_datetime(
                "2020-02-13T21:00:00.000Z"), 'McDonalds'),
        ]
    )) == 3


def test_time_difference_in_minutes_positive_difference_input():
    assert time_difference_in_minutes(
        format_str_to_datetime("2020-02-13T11:00:00.000Z"),
        format_str_to_datetime("2020-02-13T10:00:00.000Z"),
    ) == timedelta(minutes=60)


def test_time_difference_in_minutes_negative_difference_input():
    assert time_difference_in_minutes(
        format_str_to_datetime("2020-02-13T10:00:00.000Z"),
        format_str_to_datetime("2020-02-13T11:00:00.000Z"),
    ) == timedelta(minutes=60)


def test_time_difference_in_minutes_no_difference():
    assert time_difference_in_minutes(
        format_str_to_datetime("2020-02-13T10:00:00.000Z"),
        format_str_to_datetime("2020-02-13T10:00:00.000Z"),
    ) == timedelta(minutes=0)


def test_compare_transactions_returns_true():
    assert compare_transactions(
        DebitTransaction(
            TransactionTypeEnum.DEBIT,
            20,
            format_str_to_datetime("2020-02-13T10:00:00.000Z"),
            'Lanchonete da Esquina'
        ),
        DebitTransaction(
            TransactionTypeEnum.DEBIT,
            20, format_str_to_datetime("2020-02-13T10:01:59.999Z"),
            'Lanchonete da Esquina'
        )
    )


def test_compare_transactions_returns_false_by_name():
    assert not compare_transactions(
        DebitTransaction(
            TransactionTypeEnum.DEBIT,
            20,
            format_str_to_datetime("2020-02-13T10:00:00.000Z"),
            'Lanchonete da Esquina'
        ),
        DebitTransaction(
            TransactionTypeEnum.DEBIT,
            20,
            format_str_to_datetime("2020-02-13T10:01:59.999Z"),
            'Lanchonete da Outra Esquina'
        )
    )


def test_compare_transactions_returns_false_by_value():
    assert not compare_transactions(
        DebitTransaction(
            TransactionTypeEnum.DEBIT,
            2,
            format_str_to_datetime("2020-02-13T10:00:00.000Z"),
            'Lanchonete da Esquina'
        ),
        DebitTransaction(
            TransactionTypeEnum.DEBIT,
            20,
            format_str_to_datetime("2020-02-13T10:01:59.999Z"),
            'Lanchonete da Esquina'
        )
    )
