import pytest
from controllers.handlers.TransactionExecuterHandler import handle_transaction
from controllers.handlers.AccountCreatorHandler import handle_create_account
from controllers.persistence.PersistenceController import EntityKeyEnum, get_db


class TestTransactionExecuterHandler:

    def setup_class(self):
        self.account_dict = {'account': {'active-card': True,
                                         'available-limit': 100}, 'violations': []}
        get_db().set_value(EntityKeyEnum.ACCOUNT_KEY.value, self.account_dict)
        self.transaction_dict = {"transaction": {"merchant": "Burger King",
                             "amount": 20, "time": "2019-02-13T10:00:00.000Z"}}

    def teardown_class(self):
        get_db().dictMap = {}

    def test_handle_transaction(self):
        expected_dict = {'account': {'active-card': True,
                                     'available-limit': 90}, 'violations': []}

        assert handle_transaction(self.acc_dict) == expected_dict

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
