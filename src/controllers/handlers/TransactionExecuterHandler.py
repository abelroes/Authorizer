
def handle_transaction(transaction_operation: dict) -> dict:
    validation_result = transaction_operation
    validation_result["violation"] = ["bla-bla-bla"]
    return validation_result