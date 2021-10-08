from models.Account.StandardAccount import StandardAccount
from usecases.enums.ViolationEnum import ViolationEnum


def validate_card_is_active(acc: StandardAccount) -> str:
    if acc:
        return ViolationEnum.CARD_NOT_ACTIVE.value if not acc.card_status else None
    else:
        return None
