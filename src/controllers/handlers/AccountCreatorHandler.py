from usecases.AccountValidator import validate_account_operation
from adapters.InMemoryDBAdapter import InMemoryDBAdapter
from models.Account.StandardAccount import StandardAccount


def handle_create_account(account_operation: dict) -> dict:
    db = InMemoryDBAdapter()
    account = StandardAccount.from_dict(account_operation)
    account_already_existed = not db.set_value_if_not_exists(
        account.account_type.value, account.to_dict()
    )
    violations = validate_account_operation(account_already_existed, account)
    validation_result = account.to_dict()
    validation_result["violations"] = violations
    return validation_result
