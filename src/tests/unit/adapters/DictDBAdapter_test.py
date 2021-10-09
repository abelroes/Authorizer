from adapters.DictDBAdapter import DictDBAdapter


class TestDictDBAdapter:

    def setup_class(self):
        self.key_to_find = "some_key"
        self.db = DictDBAdapter()
    
    def teardown_class(self):
        self.db.remove_key(self.key_to_find)
    
    def test_set_value_puts_value_in_db(self):
        value = "value"
        self.db.set_value(self.key_to_find, value)

        assert self.db.get_value(self.key_to_find) == value

    def test_set_value_updates_value_in_db(self):
        value = self.db.get_value(self.key_to_find)
        self.db.set_value(self.key_to_find, 12345)

        assert self.db.get_value(self.key_to_find) != value
    
    def test_dictdbddapter_is_singleton(self):
        initial_db = self.db
        assert self.db.dictMap.popitem() is not None
        self.db = DictDBAdapter()
        
        assert self.db == initial_db

    def test_get_value_finds_string_in_db(self):
        value_to_find = "some_value"
        self.db.set_value(self.key_to_find, value_to_find)

        assert self.db.get_value(self.key_to_find) == value_to_find

    def test_get_value_finds_number_in_db(self):
        value_to_find = 12345
        self.db.set_value(self.key_to_find, value_to_find)

        assert self.db.get_value(self.key_to_find) == value_to_find

    def test_get_value_finds_list_in_db(self):
        value_to_find = [1, 2, 3, 4, 5]
        self.db.set_value(self.key_to_find, value_to_find)

        assert self.db.get_value(self.key_to_find) == value_to_find

    def test_get_value_finds_dict_in_db(self):
        value_to_find = {'oher_key': 'some_other_value'}
        self.db.set_value(self.key_to_find, value_to_find)

        assert self.db.get_value(self.key_to_find) == value_to_find

    def test_get_value_does_not_find_key_in_db(self):
        self.db.remove_key(self.key_to_find)
        assert self.db.get_value(self.key_to_find) is None
        assert self.db.dictMap == {}
    
    def test_get_value_does_not_find_value_for_key_in_db(self):
        self.db.set_value(self.key_to_find, None)

        assert self.db.get_value(self.key_to_find) is None
