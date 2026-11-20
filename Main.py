# IMPORT MODULES
from File_handler import load_data, save_data

from Account_management import (
    create_account,
    find_account,
    update_account,
    delete_account,
    deposit,
    withdraw,
    get_balance,
    display_accounts
)

from Transactions import (
    record_transaction,
    transfer,
    show_history
)


# LOAD BANK DATA
data = load_data()

accounts = data["accounts"]

history = data["transactions"]


# REQUIRED INPUT
def get_required_input(message):
    while True:
        value = input(message).strip()

        if value == "":
            print("Error: This field is required.")

        else:
            return value


# ACCOUNT NUMBER INPUT
def get_account_number(message):
    while True:
        number = get_required_input(message)

        if not number.isdigit():
            print("Error: Account number must contain numbers only.")

        else:
            return number


# AMOUNT INPUT
def get_amount(message):
    while True:
        value = get_required_input(message)

        try:
            amount = float(value)

            if amount <= 0:
                print("Error: Amount must be greater than zero.")

            else:
                return amount

        except ValueError:
            print("Error: Please enter a valid number.")


# INITIAL BALANCE INPUT
def get_initial_balance():
    while True:
        value = input(
            "Enter Initial Balance (Press Enter for 0): "
        ).strip()

        if value == "":
            return 0.0

        try:
            amount = float(value)

            if amount < 0:
                print("Error: Balance cannot be negative.")

            else:
                return amount

        except ValueError:
            print("Error: Please enter a valid number.")


# MAIN MENU
def main():
    while True:
        print("\n========================================")
        print("       LOCBANK MANAGEMENT SYSTEM")
        print("========================================")

        options = "[1] Create Account\n" \
                  "[2] View Accounts\n" \
                  "[3] Update Account\n" \
                  "[4] Delete Account\n" \
                  "[5] Deposit Money\n" \
                  "[6] Withdraw Money\n" \
                  "[7] Transfer Money\n" \
                  "[8] Balance Inquiry\n" \
                  "[9] Transaction History\n" \
                  "[0] Exit"
        
        print(options)

        print("========================================")

        choice = input("Enter your choice: ").strip()


        # CREATE ACCOUNT
        if choice == "1":
            print("\n========== CREATE ACCOUNT ==========")

            try:
                number = get_account_number(
                    "Enter Account Number: "
                )

                name = get_required_input(
                    "Enter Account Name: "
                )

                acc_type = get_required_input(
                    "Enter Account Type: "
                )

                initial_balance = get_initial_balance()

                account = create_account(
                    accounts,
                    number,
                    name,
                    acc_type,
                    initial_balance
                )

                save_data(data)

                print("\nAccount successfully created!")
                print("Account Number:", account["account_number"])
                print("Account Name:", account["account_name"])
                print("Account Type:", account["account_type"])
                print(
                    "Initial Balance: PHP",
                    format(account["balance"], ".2f")
                )

            except ValueError as error:
                print("\nError:", error)

        # VIEW ACCOUNTS
        elif choice == "2":
            display_accounts(accounts)

        # UPDATE ACCOUNT
        elif choice == "3":
            print("\n========== UPDATE ACCOUNT ==========")

            try:
                number = get_account_number(
                    "Enter Account Number: "
                )

                new_name = get_required_input(
                    "Enter New Account Name: "
                )

                update_account(accounts, number, new_name)

                save_data(data)

                print("\nAccount successfully updated!")

            except ValueError as error:
                print("\nError:", error)

        # DELETE ACCOUNT
        elif choice == "4":
            print("\n========== DELETE ACCOUNT ==========")

            try:
                number = get_account_number(
                    "Enter Account Number: "
                )

                account = find_account(accounts, number)

                if account is None:
                    raise ValueError("Account not found.")

                print("\nAccount Name:", account["account_name"])

                confirm = get_required_input(
                    "Are you sure you want to delete this account? (Y/N): "
                ).upper()

                if confirm == "Y":
                    delete_account(accounts, number)

                    save_data(data)

                    print("\nAccount successfully deleted!")

                elif confirm == "N":
                    print("\nAccount deletion cancelled.")

                else:
                    print("\nError: Please enter Y or N.")

            except ValueError as error:
                print("\nError:", error)

        # DEPOSIT MONEY
        elif choice == "5":
            print("\n========== DEPOSIT MONEY ==========")

            try:
                number = get_account_number(
                    "Enter Account Number: "
                )

                account = find_account(accounts, number)

                if account is None:
                    raise ValueError("Account not found.")

                amount = get_amount(
                    "Enter Deposit Amount: PHP "
                )

                previous_balance = get_balance(account)

                deposit(account, amount)

                record_transaction(
                    history,
                    "Deposit",
                    number,
                    amount,
                    "Cash Deposit"
                )

                save_data(data)

                print("\nDeposit successful!")
                print("Account Name:", account["account_name"])
                print(
                    "Previous Balance: PHP",
                    format(previous_balance, ".2f")
                )
                print(
                    "New Balance: PHP",
                    format(account["balance"], ".2f")
                )

            except ValueError as error:
                print("\nError:", error)

        # WITHDRAW MONEY
        elif choice == "6":
            print("\n========== WITHDRAW MONEY ==========")

            try:

                number = get_account_number(
                    "Enter Account Number: "
                )

                account = find_account(accounts, number)

                if account is None:
                    raise ValueError("Account not found.")

                amount = get_amount(
                    "Enter Withdrawal Amount: PHP "
                )

                previous_balance = get_balance(account)

                withdraw(account, amount)

                record_transaction(
                    history,
                    "Withdrawal",
                    number,
                    amount,
                    "Cash Withdrawal"
                )

                save_data(data)

                print("\nWithdrawal successful!")
                print("Account Name:", account["account_name"])
                print(
                    "Previous Balance: PHP",
                    format(previous_balance, ".2f")
                )
                print(
                    "New Balance: PHP",
                    format(account["balance"], ".2f")
                )

            except ValueError as error:
                print("\nError:", error)

        # TRANSFER MONEY
        elif choice == "7":
            print("\n========== TRANSFER MONEY ==========")

            try:
                sender = get_account_number(
                    "Enter Sender Account Number: "
                )

                receiver = get_account_number(
                    "Enter Receiver Account Number: "
                )

                amount = get_amount(
                    "Enter Transfer Amount: PHP "
                )

                transfer(
                    accounts,
                    history,
                    sender,
                    receiver,
                    amount
                )

                save_data(data)

                print("\nTransfer successful!")
                print("Sender Account:", sender)
                print("Receiver Account:", receiver)
                print(
                    "Transferred Amount: PHP",
                    format(amount, ".2f")
                )

            except ValueError as error:
                print("\nError:", error)

        # BALANCE INQUIRY
        elif choice == "8":
            print("\n========== BALANCE INQUIRY ==========")

            try:
                number = get_account_number(
                    "Enter Account Number: "
                )

                account = find_account(accounts, number)

                if account is None:
                    raise ValueError("Account not found.")

                print("\nAccount Name:", account["account_name"])
                print("Account Number:", account["account_number"])
                print("Account Type:", account["account_type"])
                print(
                    "Available Balance: PHP",
                    format(get_balance(account), ".2f")
                )

            except ValueError as error:
                print("\nError:", error)

        # TRANSACTION HISTORY
        elif choice == "9":
            show_history(history)

        # EXIT PROGRAM
        elif choice == "0":
            save_data(data)

            print("\nThank you for using LocBank!")
            print("Program closed.")

            break

        # INVALID MENU CHOICE
        else:
            print("\nError: Invalid menu choice.")
            print("Please select a number from 0 to 9.")


# RUN MAIN PROGRAM
if __name__ == "__main__":
    main()
