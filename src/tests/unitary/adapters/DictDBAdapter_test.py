from adapters.DictDBAdapter import DictDBAdapter


def test_get_value_finds_string_in_db():
    key_to_find = "some_key"
    value_to_find = "some_value"
    db = DictDBAdapter()
    db.set_value(key_to_find, value_to_find)

    assert db.get_value(key_to_find) == value_to_find
