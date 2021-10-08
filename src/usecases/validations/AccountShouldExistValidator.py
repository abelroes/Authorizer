from usecases.enums.ViolationEnum import ViolationEnum


def validate_account_should_exist(account_already_existed: bool) -> str:
    return (
        ViolationEnum.ACCOUNT_ALREADY_EXISTS.value if account_already_existed else None
    )
