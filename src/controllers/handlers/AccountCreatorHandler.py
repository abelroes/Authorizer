from controllers.handlers.HandlerUtils import (
    convert_dict_to_account, format_validation_result, is_account_already_exists
)
from usecases.Account.AccountValidator import validate_account_operation


def handle_create_account(account_operation: dict) -> dict:
    account = convert_dict_to_account(account_operation)
    account_already_existed = is_account_already_exists(account)
    validation_result = format_validation_result(
        validate_account_operation(account_already_existed), account
    )
    return validation_result
