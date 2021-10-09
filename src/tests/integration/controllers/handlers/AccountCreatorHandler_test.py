import pytest
from controllers.handlers.AccountCreatorHandler import handle_create_account
from controllers.persistence.PersistenceController import EntityKeyEnum, get_db


class TestAccountCreatorHandler:

    def setup_class(self):
        self.acc_dict = {'account': {
            'available-limit': 100, 'active-card': True}}

    def teardown_class(self):
        get_db().remove_key(EntityKeyEnum.ACCOUNT_KEY.value)

    def test_handle_create_account(self):
        expected_dict = {'account': {'active-card': True,
                                     'available-limit': 100}, 'violations': []}

        assert handle_create_account(self.acc_dict) == expected_dict

    def test_handle_create_account_returns_violation(self):
        expected_dict = {'account': {'active-card': True,
                                     'available-limit': 100}, 'violations': ['account-already-initialized']}

        assert handle_create_account(self.acc_dict) == expected_dict

    def test_handle_create_account_passing_empty_dict(self):
        with pytest.raises(AttributeError):
            handle_create_account({})

    def test_handle_create_account_passing_none_dict(self):
        with pytest.raises(AttributeError):
            handle_create_account(None)
