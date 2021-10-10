from adapters.DictDBAdapter import DictDBAdapter
from controllers.persistence.PersistenceController import get_db


def test_get_db_returns_db_without_initializing():
    assert get_db() is not None


def test_get_db_returns_correct_db():
    assert get_db() == DictDBAdapter()