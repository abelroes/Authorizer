from enum import Enum


class ViolationEnum(Enum):
    ACCOUNT_ALREADY_EXISTS = "account-already-initialized"
    ACCOUNT_NOT_INITIALIZED = "account-not-initialized"
    CARD_NOT_ACTIVE = "card-not-active"
    INSUFFICIENT_LIMIT = "insufficient-limit"
    HIGH_FREQUENCY = "high-frequency-small-interval"
    DOUBLE_TRANSACTION = "doubled-transaction"
