import pytest
from usecases.enums.ViolationEnum import ViolationEnum
from controllers.handlers.TransactionExecuterHandler import handle_transaction
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
                                     'available-limit': 80}, 'violations': []}

        assert handle_transaction(self.transaction_dict) == expected_dict

    def test_handle_transaction_returns_violation(self):
        expected_dict = {'account': {'active-card': True, 'available-limit': 80},
                         'violations': [ViolationEnum.DOUBLED_TRANSACTION.value]}

        assert handle_transaction(self.transaction_dict) == expected_dict

    def test_handle_transaction_passing_empty_dict(self):
        with pytest.raises(KeyError):
            handle_transaction({})

    def test_handle_transaction_passing_none_dict(self):
        with pytest.raises(TypeError):
            handle_transaction(None)
