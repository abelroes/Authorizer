from typing import List, Set
from usecases.validations.TooMuchTransactionsValidator import validate_transaction_frequency
from usecases.validations.TransactionIsNotDuplicatedValidator import validate_transaction_duplication
from usecases.validations.HasEnoughBalanceValidator import validate_account_has_balance
from usecases.validations.CardIsActiveValidator import validate_card_is_active
from models.Account.GenericAccount import GenericAccount
from models.Transaction.GenericTransaction import GenericTransaction


def validate_transaction_operation(
    account: GenericAccount,
    transaction: GenericTransaction,
    transaction_history: List[GenericTransaction],
) -> Set[str]:
    return {
        validate_card_is_active(account),
        validate_account_has_balance(account, transaction),
        validate_transaction_frequency(transaction, transaction_history),
        validate_transaction_duplication(transaction, transaction_history),
    }
