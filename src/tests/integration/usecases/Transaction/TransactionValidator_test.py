from usecases.enums.ViolationEnum import ViolationEnum
from models.formaters.DatetimeFormater import format_str_to_datetime
from models.Account.StandardAccount import StandardAccount
from models.Transaction.DebitTransaction import DebitTransaction
from models.enums.AccountTypeEnum import AccountTypeEnum
from models.enums.TransactionTypeEnum import TransactionTypeEnum
from usecases.Transaction.TransactionValidator import validate_transaction_operation


class TestTransactionValidator:
    def setup_class(self):
        self.valid_account = StandardAccount(
            AccountTypeEnum.STANDARD_ACCOUNT,
            1000,
            True
        )
        self.invalid_account = StandardAccount(
            AccountTypeEnum.STANDARD_ACCOUNT,
            0,
            False
        )
        self.valid_transaction = DebitTransaction(
            TransactionTypeEnum.DEBIT,
            10,
            format_str_to_datetime("2020-02-14T10:00:00.000Z"),
            'Starbucks'
        )
        self.invalid_transaction = DebitTransaction(
            TransactionTypeEnum.DEBIT,
            99999,
            format_str_to_datetime("2020-02-14T10:00:00.000Z"),
            'Starbucks'
        )
        self.filled_transaction_history = [
            DebitTransaction(TransactionTypeEnum.DEBIT, 10, format_str_to_datetime(
                "2020-02-13T10:00:00.000Z"), 'Lanchonete da Esquina'),
            DebitTransaction(TransactionTypeEnum.DEBIT, 10, format_str_to_datetime(
                "2020-02-13T11:00:00.000Z"), 'PF do João'),
            DebitTransaction(TransactionTypeEnum.DEBIT, 1000, format_str_to_datetime(
                "2020-02-13T21:00:00.000Z"), 'Restaurante Chic'),
        ]

    def test_validate_transaction_operation(self):
        assert validate_transaction_operation(
            self.valid_account,
            self.valid_transaction,
            self.filled_transaction_history
        ) == {None}

    def test_validate_transaction_operation_with_empty_history(self):
        assert validate_transaction_operation(
            self.valid_account,
            self.valid_transaction,
            []
        ) == {None}

    def test_validate_transaction_operation_with_invalid_account(self):
        assert validate_transaction_operation(
            self.invalid_account,
            self.valid_transaction,
            self.filled_transaction_history
        ) == {None, ViolationEnum.CARD_NOT_ACTIVE.value, ViolationEnum.INSUFFICIENT_LIMIT.value}

    def test_validate_transaction_operation_with_invalid_transaction(self):
        assert validate_transaction_operation(
            self.valid_account,
            self.invalid_transaction,
            self.filled_transaction_history
        ) == {None, ViolationEnum.INSUFFICIENT_LIMIT.value}
