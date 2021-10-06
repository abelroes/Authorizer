from enum import Enum
from adapters.GenericDatabaseAdapter import GenericDatabaseAdapter
from adapters.DictDBAdapter import DictDBAdapter


class EntityKeyEnum(Enum):
    ACCOUNT_KEY = "account"
    TRANSACTION_HISTORY_KEY = "transaction_history"


def get_db() -> GenericDatabaseAdapter:
    return DictDBAdapter()
