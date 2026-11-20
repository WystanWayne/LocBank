from Account_management import find_account, withdraw, deposit


# RECORD TRANSACTION
def record_transaction(history, transaction_type, account_number, amount, details=""):
    transaction = {
        "type": transaction_type,
        "account_number": account_number,
        "amount": amount,
        "details": details
    }

    history.append(transaction)


# TRANSFER MONEY
def transfer(accounts, history, sender_number, receiver_number, amount):
    if not sender_number.strip():
        raise ValueError("Sender account number is required.")

    if not receiver_number.strip():
        raise ValueError("Receiver account number is required.")

    if amount <= 0:
        raise ValueError("Transfer amount must be greater than zero.")

    if sender_number == receiver_number:
        raise ValueError("Cannot transfer to the same account.")

    sender = find_account(accounts, sender_number)

    receiver = find_account(accounts, receiver_number)

    if sender is None:
        raise ValueError("Sender account not found.")

    if receiver is None:
        raise ValueError("Receiver account not found.")

    if amount > sender["balance"]:
        raise ValueError("Insufficient balance.")

    withdraw(sender, amount)

    deposit(receiver, amount)

    record_transaction(
        history,
        "Transfer",
        sender_number,
        amount,
        "To Account " + receiver_number
    )

    record_transaction(
        history,
        "Transfer",
        receiver_number,
        amount,
        "From Account " + sender_number
    )

    return True


# SHOW TRANSACTION HISTORY
def show_history(history, limit=10):
    if not history:
        print("\nNo transactions found.")
        return

    print("\n========== TRANSACTION HISTORY ==========")

    for transaction in history[-limit:]:
        print(
            "Type:", transaction["type"],
            "| Account:", transaction["account_number"],
            "| Amount: PHP", format(transaction["amount"], ".2f"),
            "| Details:", transaction["details"]
        )
