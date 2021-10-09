import pytest
from controllers.handlers.AuthorizerHandler import authorize_operation, handle_input
from controllers.persistence.PersistenceController import get_db


class TestAuthorizerHandlerIntegration():

    def setup_class(self):
        self.operations_list = [
            {"account": {"active-card": True, "available-limit": 100}},
            {"transaction": {"merchant": "Burger King",
                             "amount": 20, "time": "2019-02-13T10:00:00.000Z"}},
            {"transaction": {"merchant": "Habbib's", "amount": 20,
                             "time": "2019-02-13T11:00:00.000Z"}},
            {"transaction": {"merchant": "McDonald's",
                             "amount": 30, "time": "2019-02-13T12:00:00.000Z"}},
        ]

    def teardown_class(self):
        get_db().dictMap = {}

    def test_handle_input(self):
        expected_output = [
            {'account': {'active-card': True, 'available-limit': 100}, 'violations': []},
            {'account': {'active-card': True, 'available-limit': 80}, 'violations': []},
            {'account': {'active-card': True, 'available-limit': 60}, 'violations': []},
            {'account': {'active-card': True, 'available-limit': 30}, 'violations': []}
        ]

        assert handle_input(self.operations_list) == expected_output

    def test_handle_input_empty_list(self):
        expected_output = []

        assert handle_input(expected_output) == expected_output

    def test_handle_input_None_list(self):
        with pytest.raises(TypeError):
            handle_input(None)

    def test_handle_input_invalid_dict_in_list(self):
        invalid_list = [
            {'invalid_dict_key': 'some_value'}
        ]

        with pytest.raises(IndexError):
            handle_input(invalid_list)

    def test_handle_input_not_a_dict_in_list(self):
        invalid_list = [
            ['invalid_dict']
        ]

        with pytest.raises(AttributeError):
            handle_input(invalid_list)

    def test_authorize_account_operation(self):
        self.teardown_class()
        expected_output = {'account': {'active-card': True,
                                       'available-limit': 100}, 'violations': []}

        assert authorize_operation(self.operations_list[0]) == expected_output

    def test_authorize_fail_account_operation(self):
        expected_output = {'account': {
            'active-card': True, 'available-limit': 100}, 'violations': ['account-already-initialized']}

        assert authorize_operation(self.operations_list[0]) == expected_output
