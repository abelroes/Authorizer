import pytest
from functools import reduce
from models.formaters.DatetimeFormater import format_str_to_datetime
from models.Transaction.DebitTransaction import DebitTransaction
from models.enums.TransactionTypeEnum import TransactionTypeEnum
from controllers.handlers.HandlerUtils import (
    convert_dict_to_account, convert_dict_to_transaction,
    format_validation_result, get_saved_account, get_transaction_history, is_account_already_exists, save_account_changes
)
from controllers.persistence.PersistenceController import EntityKeyEnum, get_db
from models.Account.StandardAccount import StandardAccount
from models.enums.AccountTypeEnum import AccountTypeEnum


class TestHandlerUtils():

    def setup_class(self):
        date_and_time = "2019-02-13T10:00:00.000Z"
        self.standard_account = StandardAccount(
            AccountTypeEnum.STANDARD_ACCOUNT,
            100,
            True
        )
        self.debit_transaction = DebitTransaction(
            TransactionTypeEnum.DEBIT,
            10,
            format_str_to_datetime(date_and_time),
            "Burger King"
        )
        self.transaction_history = [
            {"transaction": {"merchant": "Burger King",
                             "amount": 20, "time": "2019-02-13T10:00:00.000Z"}},
            {"transaction": {"merchant": "Habbib's", "amount": 10,
                             "time": "2019-02-13T11:00:00.000Z"}},
            {"transaction": {"merchant": "McDonald's",
                             "amount": 30, "time": "2019-02-13T12:00:00.000Z"}}
        ]
        get_db().set_value(
            EntityKeyEnum.TRANSACTION_HISTORY_KEY.value,
            self.transaction_history
        )

    def teardown_class(self):
        get_db().dictMap = {}

    def test_convert_dict_to_account(self):
        acc_dict = {'account': {'available-limit': 100, 'active-card': True}}

        assert convert_dict_to_account(acc_dict) == self.standard_account

    def test_convert_dict_to_account_with_None_value(self):
        acc_dict = None
        assert convert_dict_to_account(acc_dict) is None

    def test_convert_dict_to_account_with_empty_dict(self):
        acc_dict = {}
        assert convert_dict_to_account(acc_dict) is None

    def test_is_account_already_exists_returns_false(self):
        assert not is_account_already_exists(self.standard_account)

    def test_is_account_already_exists_returns_true(self):
        get_db().set_value(self.standard_account.account_type.value,
                           self.standard_account.to_dict())

        assert is_account_already_exists(self.standard_account)

    def test_format_validation_result(self):
        violations = {'some_violation', 'some_other_violation', 'another_one'}
        expected_dict = {'account': {'active-card': True, 'available-limit': 100},
                         'violations': ['some_violation', 'some_other_violation', 'another_one']}

        result = format_validation_result(violations, self.standard_account)
        assert result['account'] == expected_dict['account']
        assert reduce(lambda a, b: a and b, list(
            map(lambda it: it in list(expected_dict['violations']), result['violations'])))

    def test_format_validation_result_with_filled_violations_and_None_value(self):
        violations = {'some_violation',
                      'some_other_violation', 'another_one', None}
        expected_dict = {'account': {'active-card': True, 'available-limit': 100},
                         'violations': ['some_violation', 'some_other_violation', 'another_one']}

        result = format_validation_result(violations, self.standard_account)
        assert result['account'] == expected_dict['account']
        assert reduce(lambda a, b: a and b, list(
            map(lambda it: it in list(expected_dict['violations']), result['violations'])))

    def test_format_validation_result_with_None_value_in_violations_set(self):
        violations = {None}
        expected_dict = {'account': {'active-card': True, 'available-limit': 100},
                         'violations': []}

        assert format_validation_result(
            violations, self.standard_account) == expected_dict

    def test_format_validation_result_with_None_value_as_violations(self):
        violations = None

        with pytest.raises(TypeError):
            format_validation_result(
                violations, self.standard_account)

    def test_format_validation_result_with_empty_value_as_account(self):
        violations = {}

        with pytest.raises(TypeError):
            format_validation_result(
                violations, StandardAccount())

    def test_format_validation_result_with_None_value_as_account(self):
        violations = {}

        with pytest.raises(TypeError):
            format_validation_result(
                violations, None)

    def test_convert_dict_to_transaction(self):
        transaction_dict = {"transaction": {"merchant": "Burger King",
                                            "amount": 10, "time": "2019-02-13T10:00:00.000Z"}}

        assert convert_dict_to_transaction(
            transaction_dict) == self.debit_transaction

    def test_convert_dict_to_transaction_with_None_value(self):
        with pytest.raises(TypeError):
            convert_dict_to_transaction(None)

    def test_convert_dict_to_transaction_with_empty_dict(self):
        with pytest.raises(KeyError):
            convert_dict_to_transaction({})

    def test_get_saved_account(self):
        get_db().set_value(
            self.standard_account.account_type.value,
            self.standard_account.to_dict()
        )

        assert get_saved_account() == self.standard_account.to_dict()

    def test_get_transaction_history(self):
        transactions = list(
            map(lambda trans: DebitTransaction.from_dict(trans), self.transaction_history))
        assert get_transaction_history() == transactions

    def test_get_saved_account_not_existing_one_in_db(self):
        self.teardown_class()
        assert get_saved_account() == None

    def test_get_transaction_history_not_existing_one_in_db(self):
        self.teardown_class()
        assert get_transaction_history() == []

    def test_save_account_changes(self):
        transaction_to_save_dict = self.transaction_history[0]
        save_account_changes(
            self.standard_account, DebitTransaction.from_dict(transaction_to_save_dict))

        assert transaction_to_save_dict in get_db().get_value(
            EntityKeyEnum.TRANSACTION_HISTORY_KEY.value
        )
        assert get_db().get_value(
            EntityKeyEnum.ACCOUNT_KEY.value) == self.standard_account.to_dict()

    def test_save_account_changes_without_account(self):
        transaction_to_save_dict = self.transaction_history[0]
        with pytest.raises(AttributeError):
            save_account_changes(
                None, DebitTransaction.from_dict(transaction_to_save_dict))

    def test_save_account_changes_without_transaction(self):
        with pytest.raises(AttributeError):
            save_account_changes(self.standard_account, None)

    def test_save_account_changes_without_values(self):
        with pytest.raises(AttributeError):
            save_account_changes(None, None)
