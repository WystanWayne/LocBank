# TRANSACTION TYPES
TRANSACTION_TYPES = ("Deposit", "Withdrawal", "Transfer")


# FIND ACCOUNT
def find_account(accounts, number):
    for account in accounts:
        if account["account_number"] == number:
            return account

    return None


# CREATE ACCOUNT
def create_account(accounts, number, name, acc_type="Savings", initial_balance=0.0):

    if not number.strip():
        raise ValueError("Account number is required.")

    if not number.isdigit():
        raise ValueError("Account number must contain numbers only.")

    if not name.strip():
        raise ValueError("Account name is required.")

    if not acc_type.strip():
        raise ValueError("Account type is required.")

    if find_account(accounts, number):
        raise ValueError("Account number already exists.")

    if initial_balance < 0:
        raise ValueError("Initial balance cannot be negative.")

    account = {
        "account_number": number,
        "account_name": name,
        "account_type": acc_type,
        "balance": initial_balance
    }

    accounts.append(account)

    return account


# UPDATE ACCOUNT
def update_account(accounts, number, new_name):
    if not number.strip():
        raise ValueError("Account number is required.")

    if not new_name.strip():
        raise ValueError("New account name is required.")

    account = find_account(accounts, number)

    if account is None:
        raise ValueError("Account not found.")

    account.update({
        "account_name": new_name
    })


# DELETE ACCOUNT
def delete_account(accounts, number):
    if not number.strip():
        raise ValueError("Account number is required.")

    account = find_account(accounts, number)

    if account is None:
        raise ValueError("Account not found.")

    accounts.remove(account)


# DEPOSIT MONEY
def deposit(account, amount):
    if amount <= 0:
        raise ValueError("Deposit amount must be greater than zero.")

    account["balance"] += amount

    return account["balance"]


# WITHDRAW MONEY
def withdraw(account, amount):
    if amount <= 0:
        raise ValueError("Withdrawal amount must be greater than zero.")

    if amount > account["balance"]:
        raise ValueError("Insufficient balance.")

    account["balance"] -= amount

    return account["balance"]


# GET BALANCE
def get_balance(account):
    return account["balance"]


# DISPLAY ACCOUNTS
def display_accounts(accounts, limit=5):
    if not accounts:
        print("\nNo accounts available.")
        return

    print("\n========== BANK ACCOUNTS ==========")

    for account in accounts[:limit]:
        print(
            "Account Number:", account["account_number"],
            "| Name:", account["account_name"],
            "| Type:", account["account_type"],
            "| Balance: PHP", format(account["balance"], ".2f")
        )

    print("\nTotal Accounts:", len(accounts))

    total_balance = sum(
        account["balance"] for account in accounts
    )

    print("Total Balance: PHP", format(total_balance, ".2f"))


# SHOW MESSAGES
def show_messages(*messages):
    for message in messages:
        print(message)
