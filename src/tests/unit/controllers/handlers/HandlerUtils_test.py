import pytest
from functools import reduce
from controllers.handlers.HandlerUtils import convert_dict_to_account, format_validation_result, is_account_already_exists
from controllers.persistence.PersistenceController import get_db
from models.Account.StandardAccount import StandardAccount
from models.enums.AccountTypeEnum import AccountTypeEnum


class TestHandlerUtils():

    def setup_class(self):
        self.standard_account = StandardAccount(
            AccountTypeEnum.STANDARD_ACCOUNT,
            100,
            True
        )

    def teardown_class(self):
        get_db().remove_key(self.standard_account.account_type.value)

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
