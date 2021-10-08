from usecases.Transaction.TransactionValidationUtils import positive_balance_after_transaction
from models.Account.StandardAccount import StandardAccount
from models.Transaction.DebitTransaction import DebitTransaction
from usecases.enums.ViolationEnum import ViolationEnum


def validate_account_has_balance(acc: StandardAccount, trans: DebitTransaction) -> str:
    if acc:
        return (
            ViolationEnum.INSUFFICIENT_LIMIT.value
            if not positive_balance_after_transaction(acc, trans)
            else None
        )
    else:
        return None
