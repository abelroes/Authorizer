from typing import Set
from usecases.validations.AccountShouldExistValidator import validate_account_should_exist


def validate_account_operation(account_already_existed: bool) -> Set[str]:
    return {validate_account_should_exist(account_already_existed)}
