from usecases.enums.ViolationEnum import ViolationEnum


def validate_account_is_initialized(account_already_existed: bool) -> str:
    return (
        ViolationEnum.ACCOUNT_NOT_INITIALIZED.value
        if not account_already_existed
        else None
    )
