    # LocBank: Banking Management System
    ## CS 26 – Exam 2 Technical Documentation

    **Document type:** Program technical documentation
    **Course coverage:** Weeks 4–5 Python concepts
    **Program type:** GUI-based banking transaction management

    ## 1. Program Title and Overview
    **LocBank** is a Python banking management program with a graphical user interface built using `tkinter`. It is intended for bank customers, bank staff, and administrators, with a separate screen for each role after login. Its main purpose is to replace error-prone manual record keeping with an organized system for managing customer accounts and basic banking transactions.

    With LocBank, users can create accounts, deposit and withdraw money, transfer funds between accounts, check balances, and view transaction history. The program stores records in Python lists and dictionaries, separates the interface from the banking logic using multiple modules, saves data in a JSON file, and uses exception handling to reject invalid input.

    ## 2. Problem Description
    Managing bank accounts and transactions manually is slow and error-prone. Handwritten records can contain calculation mistakes, get misplaced, and make it hard to trace earlier transactions. Checking a balance or updating several accounts after a transfer takes longer when records are not organized.

    LocBank addresses this by storing account data in structured Python collections, validating every transaction before it is applied, and saving records to a file so they persist between runs.

    **Input** Account number, account holder's name, account type, initial balance, transaction amount, sender account number, receiver account number, login credentials

    **Processing** Validate inputs, create accounts, apply deposits and withdrawals, transfer money between accounts, update balances, record each transaction, save to file

    **Output** Account records, updated balances, transaction confirmations or error messages, transfer results, transaction history

    ## 3. Program Objectives
    1. Create and store multiple bank accounts, each with a unique account number, holder name, account type, and balance.
    2. Process deposits and withdrawals only when the account exists and the amount is greater than zero (and, for withdrawals, not more than the balance).
    3. Transfer money between two existing accounts so that the amount deducted from the sender equals the amount added to the receiver.
    4. Display the account information and current balance when a valid account number is entered.
    5. Record every deposit, withdrawal, and transfer, and display the transaction history.

    ## 4. Program Requirements and Features

    ### 4.1 Features and Functions
    - **Account management:** Staff and administrators can create a bank account by entering an account number, the holder's name, an account type (such as Savings), and a starting balance. The program checks that the account number is not already used and that the name and type are not blank before saving the account.
    - **Deposit:** Adds a positive amount to an existing account and updates its balance.
    - **Withdrawal:** Subtracts an amount from an account, but only if the amount is greater than zero and not more than the current balance.
    - **Fund transfer:** Moves money from a sender's account to a different, existing receiver's account. The sender's balance goes down and the receiver's balance goes up by the same amount.
    - **Balance inquiry:** Shows the account holder's details and current balance when a valid account number is entered.
    - **Transaction history:** Records every deposit, withdrawal, and transfer so users can review past activity.
    - **Role-based login:** After logging in, customers, staff, and administrators each see their own screen.
    - **Saving and loading data:** Accounts and transactions are saved to `Bank_data.json`, so they are still available the next time the program is opened.

    ### 4.2 Rules
    - Every account number must be different from all others.
    - The account holder's name and account type cannot be left blank.
    - Every amount must be more than zero.
    - A withdrawal or transfer cannot be more than the money in the account.
    - A transfer must be between two existing accounts, and they cannot be the same account.

    ### 4.3 Limitations
    LocBank is a practice project, so it does not connect to real banks. It also does not include online banking, ATM features, loans, or other currencies. All amounts use one currency.

    ### 4.4 Planned Enhancements
    These are not built yet and may be added later:
    - Searching for accounts
    - Printable transaction reports
    - Automatic backup of the data file
    - Safer password storage

    ## 5. Program Structure and Modules

    ```text
    LocBank/
    │
    ├── Main.py                  # entry point
    ├── LogIn_GUI.py             # login window
    ├── Layout.py                # shared GUI layout/styling
    │
    ├── Users_GUI.py             # customer screen
    ├── Staff_GUI.py             # staff screen
    ├── Administrator_GUI.py     # administrator screen
    │
    ├── Account_management.py    # account creation, deposit, withdraw, balance
    ├── Transactions.py          # transfer and transaction recording
    ├── File_handler.py          # save/load JSON data
    │
    └── data/
        └── Bank_data.json       # created when records are saved
    ```

    | File | Purpose |
    |---|---|
    | `Main.py` | Starts the program, loads saved data, and opens the login window. |
    | `LogIn_GUI.py` | Displays the login window and opens the correct screen for the user's role. |
    | `Layout.py` | Holds shared GUI layout and style settings used by the other GUI files. |
    | `Users_GUI.py` | Customer screen: balance inquiry, deposit, withdrawal, transfer, history. |
    | `Staff_GUI.py` | Staff screen: create and manage customer accounts and process transactions. |
    | `Administrator_GUI.py` | Administrator screen: full account management and record viewing. |
    | `Account_management.py` | Banking logic for creating accounts, deposits, withdrawals, and balance lookups. |
    | `Transactions.py` | Transfer logic and recording of transaction history. |
    | `File_handler.py` | Saving and loading account and transaction records using JSON. |
    | `data/Bank_data.json` | Stores records between runs. |

    ### How the modules connect
    The GUI modules import banking functions and call them when the user presses a button. The banking modules contain no GUI code, which keeps the logic separate from the interface and easier to test.

    ```python
    # In Users_GUI.py (example)
    from Account_management import deposit, withdraw, get_balance
    from Transactions import transfer
    from File_handler import save_data
    ```

    ## 6. Data Structures Used

    ### 6.1 List
    A list holds all account records and the transaction history. A list fits because records are added over time and kept in order.

    ```python
    accounts = []
    accounts.append({
        "account_number": "1001",
        "account_name": "<Lorence Suizo>",
        "account_type": "Savings",
        "balance": 5000.00
    })
    ```

    ### 6.2 Dictionary
    A dictionary stores the details of one account, so each piece of information is read by a meaningful key rather than a numeric position.

    ```python
    account = {
        "account_number": "1001",
        "account_name": "Lorence Suizo",
        "account_type": "Savings",
        "balance": 5000.00
    }
    print(account["balance"])   # 5000.0
    ```

    A transaction record is also a dictionary:

    ```python
    transaction = {
        "type": "Deposit",
        "account_number": "1001",
        "amount": 1000.00
    }
    ```

    ### 6.3 Tuple
    A tuple holds the fixed transaction categories. A tuple fits because these values should not change while the program runs.

    ```python
    TRANSACTION_TYPES = ("Deposit", "Withdrawal", "Transfer")

    if transaction["type"] not in TRANSACTION_TYPES:
        raise ValueError("Unknown transaction type")
    ```

    ## 7. Functions and Responsibilities

    | Function | Module | Parameters | Returns | Purpose |
    |---|---|---|---|---|
    | `create_account` | `Account_management.py` | `accounts, number, name, acc_type, balance` | New account dictionary | Validates and creates a new account |
    | `find_account` | `Account_management.py` | `accounts, number` | Account dictionary | Looks up an account; raises `ValueError` if not found |
    | `deposit` | `Account_management.py` | `account, amount` | Updated balance (`float`) | Adds money to an account |
    | `withdraw` | `Account_management.py` | `account, amount` | Updated balance (`float`) | Checks funds and deducts money |
    | `get_balance` | `Account_management.py` | `account` | Balance (`float`) | Returns the current balance |
    | `transfer` | `Transactions.py` | `sender, receiver, amount` | `None` | Moves money between two accounts |
    | `record_transaction` | `Transactions.py` | `history, type, account_number, amount` | `None` | Appends a record to the history |
    | `save_data` | `File_handler.py` | `data, filename` | `None` | Writes records to JSON |
    | `load_data` | `File_handler.py` | `filename` | `dict` or `list` | Reads saved records |

    ### 7.1 Example: `withdraw`

    ```python
    def withdraw(account, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero")
        if amount > account["balance"]:
            raise ValueError("Insufficient balance")

        account["balance"] -= amount
        return account["balance"]
    ```

    The function first rejects non-positive amounts, then rejects amounts larger than the balance. Only when both checks pass does it subtract the amount. Because the checks come first, a failed withdrawal leaves the balance unchanged.

    ### 7.2 Example: `transfer`

    ```python
    def transfer(sender, receiver, amount):
        if sender["account_number"] == receiver["account_number"]:
            raise ValueError("Cannot transfer to the same account")

        withdraw(sender, amount)    # validates amount and funds
        deposit(receiver, amount)
    ```

    The transfer reuses `withdraw` and `deposit`, so the validation rules are written once. If the withdrawal fails, the exception stops the function before the receiver is credited, so money is never added without being deducted.

    ## 8. File Handling Procedures
    LocBank saves data in a JSON text file, `data/Bank_data.json`, using Python's built-in `json` module. JSON can represent the program's lists and dictionaries directly.

    ```python
    import json

    def save_data(data, filename="data/Bank_data.json"):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)


    def load_data(filename="data/Bank_data.json"):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return []
    ```

    | Item | Explanation |
    |---|---|
    | File name and format | `Bank_data.json`, JSON text |
    | Write mode `"w"` | Creates the file or replaces its contents when saving |
    | Read mode `"r"` | Reads saved records at startup |
    | `with open(...)` | Closes the file automatically, even if an error occurs |
    | `encoding="utf-8"` | Keeps text handling consistent |
    | Missing file | `load_data` returns an empty list so the program starts with no accounts |
    | Damaged file | `json.load()` raises `json.JSONDecodeError`; the program reports this to the user instead of treating the data as valid |
    | Persistence | Yes, records persist between runs |

    ## 9. Error Handling
    LocBank expects these errors, which are **input-validation errors** (caused by the user) and are caught and shown to the user:

    - Empty account holder name or account type
    - Duplicate account number
    - Account number that does not exist
    - Letters or symbols in a numeric field
    - Zero or negative amount
    - Withdrawal or transfer larger than the balance
    - Missing or damaged data file

    ```python
    from tkinter import messagebox

    try:
        amount = float(amount_entry.get())
        new_balance = deposit(account, amount)
        messagebox.showinfo("Success", f"New balance: {new_balance:.2f}")
    except ValueError as error:
        messagebox.showerror("Invalid transaction", str(error))
    ```

    `float()` raises `ValueError` for text such as `"abc"`, and `deposit()` raises `ValueError` for amounts of zero or less. One `except ValueError` block handles both and shows the message in a message box.

    **Programming errors** (for example, a wrong variable name causing `NameError`, or `KeyError` from a typo in a dictionary key) are not caught by these blocks. They are deliberately left visible so they can be found and fixed rather than hidden by a bare `except:`.

    ## 10. Testing, Debugging, and Results

    ### 10.1 Test Cases

    | Test ID | Type | Scenario | Input | Expected Result | Actual Result | Status |
    |---|---|---|---|---|---|---|
    | T01 | Normal | Create a valid account | 1001, Alex Santos, Savings, 5000.00 | Account created with correct details and balance | Account created; balance shown as 5000.00 | Pass |
    | T02 | Normal | Deposit money | Account 1001, 1000.00 | Balance goes from 5000.00 to 6000.00 | Balance changed to 6000.00 | Pass |
    | T03 | Normal | Withdraw money | Account 1001, 500.00 | Balance goes from 6000.00 to 5500.00 | Balance changed to 5500.00 | Pass |
    | T04 | Normal | Transfer money | 1000.00 from 1001 (5000.00) to 1002 (2000.00) | Sender 4000.00, receiver 3000.00 | Sender 4000.00, receiver 3000.00 | Pass |
    | T05 | Boundary | Withdraw the exact balance | Balance 500.00, withdraw 500.00 | Withdrawal accepted, balance 0.00 | Withdrawal accepted; balance 0.00 | Pass |
    | T06 | Boundary | Deposit zero | Account 1001, 0 | Rejected with an error message | Error message shown; balance unchanged | Pass |
    | T07 | Invalid | Negative deposit | Account 1001, -100.00 | Rejected with an error message; balance unchanged | Error message shown; balance unchanged | Pass |
    | T08 | Invalid | Withdraw more than balance | Balance 500.00, withdraw 1000.00 | Rejected; balance stays 500.00 | "Insufficient balance" shown; balance 500.00 | Pass |
    | T09 | Invalid | Nonexistent account | Account 9999 | "Account not found" message | "Account not found" message shown | Pass |
    | T10 | Invalid | Duplicate account number | Create 1001 a second time | Rejected with an error message | Error message shown; no second account created | Pass |
    | T11 | Invalid | Text in amount field | Amount: `abc` | Error message, no crash | Error message shown; program kept running | Pass |
    | T12 | File | Data persists after restart | Create an account, close, reopen | Account is still listed | Account still listed after reopening | Pass |

    All 12 test cases passed.

    ### 10.2 Debugging and Verification
    No defects were observed during testing, so no code corrections were needed. The program was verified in these ways:

    - **Transfer check:** the sender started at 5000.00 and the receiver at 2000.00. After transferring 1000.00, they had 4000.00 and 3000.00, and the combined total stayed at 7000.00, so no money was created or lost.
    - **Failed transactions:** after each rejected deposit, withdrawal, and transfer (T06–T08), the balance was checked and was unchanged, confirming that validation runs before any balance is updated.
    - **Restart check:** the program was closed and reopened (T12) to confirm the saved records in `Bank_data.json` were loaded correctly.

    ## 11. Conclusion
    LocBank organizes basic banking operations (accounts, deposits, withdrawals, transfers, balance inquiry, and transaction history) behind a Python GUI. It applies lists, dictionaries, and tuples to hold data, functions and separate modules to keep the logic apart from the interface, JSON for file storage, and `try`/`except` for validation.

    **Limitations:** The program is a learning project. It has no connection to real banks, does not support multiple currencies, and its login system is basic.

    **Possible improvements:**
    1. Add account search and filtering, plus printable transaction reports.
    2. Add automatic backup of `Bank_data.json` before overwriting, and hash stored passwords.

    ## 12. References
    - Python Software Foundation. *Python 3 Documentation*. https://docs.python.org/3/
    - Python Software Foundation. *The Python Tutorial – Data Structures*. https://docs.python.org/3/tutorial/datastructures.html
    - Python Software Foundation. *The Python Tutorial – Input and Output*. https://docs.python.org/3/tutorial/inputoutput.html
    - Python Software Foundation. *`json` module documentation*. https://docs.python.org/3/library/json.html
    - Python Software Foundation. *`tkinter` documentation*. https://docs.python.org/3/library/tkinter.html