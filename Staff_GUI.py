
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# JSON database
DATA_FOLDER = "data"
DATA_FILE = os.path.join(DATA_FOLDER, "bank_data.json")


# Load and save JSON data
def load_data():
    os.makedirs(DATA_FOLDER, exist_ok=True)

    if not os.path.exists(DATA_FILE):
        default_data = {
            "users": [
                {
                    "username": "user01",
                    "password": "user123",
                    "role": "user",
                    "fullname": "Customer One"
                }
            ],
            "accounts": [
                {
                    "account_number": "1001",
                    "username": "user01",
                    "name": "Customer One",
                    "account_type": "Savings",
                    "balance": 5000.00
                }
            ],
            "transactions": []
        }

        save_data(default_data)

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        for key in ("users", "accounts", "transactions"):
            if not isinstance(data.get(key), list):
                data[key] = []

        return data

    except (json.JSONDecodeError, OSError) as error:
        messagebox.showerror("Database Error", str(error))
        return {"users": [], "accounts": [], "transactions": []}


def save_data(data):
    os.makedirs(DATA_FOLDER, exist_ok=True)

    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        return True

    except OSError as error:
        messagebox.showerror("Save Error", str(error))
        return False


# Main Staff GUI
class StaffGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LocBank - Staff Management")
        self.root.geometry("1150x700")
        self.root.minsize(950, 600)
        self.root.configure(bg="#F3F4F6")

        self.data = load_data()

        self.setup_styles()
        self.create_sidebar()
        self.create_main_area()
        self.show_dashboard()

    # GUI styles
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="white",
            foreground="#1F2937",
            rowheight=32,
            fieldbackground="white",
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#E5E7EB",
            foreground="#111827",
            font=("Arial", 10, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", "#DBEAFE")],
            foreground=[("selected", "#111827")]
        )

    # Sidebar
    def create_sidebar(self):
        self.sidebar = tk.Frame(
            self.root,
            bg="#172554",
            width=230
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="LOCBANK",
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#172554"
        ).pack(pady=(30, 5))

        tk.Label(
            self.sidebar,
            text="BANK STAFF / MANAGER",
            font=("Arial", 9),
            fg="#BFDBFE",
            bg="#172554"
        ).pack(pady=(0, 35))

        self.add_menu_button("Dashboard", self.show_dashboard)
        self.add_menu_button("Bank Accounts", self.show_accounts)
        self.add_menu_button("Customer Information", self.show_customers)
        self.add_menu_button("Transaction History", self.show_transactions)

        tk.Frame(self.sidebar, bg="#172554").pack(expand=True, fill="both")

        self.add_menu_button("Refresh Data", self.refresh_data)
        self.add_menu_button("Exit", self.exit_program)

    def add_menu_button(self, text, command):
        tk.Button(
            self.sidebar,
            text=text,
            font=("Arial", 11),
            fg="white",
            bg="#1E3A8A",
            activebackground="#2563EB",
            activeforeground="white",
            relief="flat",
            anchor="w",
            padx=25,
            pady=13,
            cursor="hand2",
            command=command
        ).pack(fill="x", padx=12, pady=4)

    # Main content area
    def create_main_area(self):
        self.main_area = tk.Frame(
            self.root,
            bg="#F3F4F6"
        )
        self.main_area.pack(
            side="right",
            fill="both",
            expand=True
        )

    def clear_main_area(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    def create_header(self, title, subtitle):
        header = tk.Frame(self.main_area, bg="#F3F4F6")
        header.pack(fill="x", padx=30, pady=(25, 15))

        tk.Label(
            header,
            text=title,
            font=("Arial", 22, "bold"),
            fg="#172554",
            bg="#F3F4F6"
        ).pack(anchor="w")

        tk.Label(
            header,
            text=subtitle,
            font=("Arial", 10),
            fg="#6B7280",
            bg="#F3F4F6"
        ).pack(anchor="w", pady=(5, 0))

    # Dashboard
    def show_dashboard(self):
        self.clear_main_area()
        self.data = load_data()

        self.create_header(
            "Staff Dashboard",
            "Welcome to the LocBank Banking Management System."
        )

        accounts = self.data["accounts"]
        users = self.data["users"]
        transactions = self.data["transactions"]

        total_balance = sum(
            float(account.get("balance", 0))
            for account in accounts
        )

        self.create_stat_cards([
            ("Total Accounts", len(accounts), "#2563EB"),
            ("Total Customers", sum(
                1 for user in users if user.get("role") == "user"
            ), "#059669"),
            ("Transactions", len(transactions), "#7C3AED"),
            ("Total Deposits", f"PHP {total_balance:,.2f}", "#D97706")
        ])

        section = tk.Frame(self.main_area, bg="#F3F4F6")
        section.pack(fill="both", expand=True, padx=30, pady=15)

        tk.Label(
            section,
            text="Recent Bank Accounts",
            font=("Arial", 14, "bold"),
            bg="#F3F4F6",
            fg="#172554"
        ).pack(anchor="w", pady=(5, 12))

        self.create_account_table(section, height=8)

    def create_stat_cards(self, cards):
        container = tk.Frame(self.main_area, bg="#F3F4F6")
        container.pack(fill="x", padx=25, pady=10)

        for title, value, color in cards:
            card = tk.Frame(
                container,
                bg="white",
                highlightbackground="#E5E7EB",
                highlightthickness=1
            )
            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=5
            )

            tk.Label(
                card,
                text=title,
                font=("Arial", 10),
                fg="#6B7280",
                bg="white"
            ).pack(anchor="w", padx=15, pady=(15, 5))

            tk.Label(
                card,
                text=str(value),
                font=("Arial", 17, "bold"),
                fg=color,
                bg="white"
            ).pack(anchor="w", padx=15, pady=(0, 15))

    # Account table
    def create_account_table(self, parent, height=12):
        columns = (
            "account_number",
            "name",
            "account_type",
            "balance"
        )

        table = ttk.Treeview(
            parent,
            columns=columns,
            show="headings",
            height=height
        )

        table.heading("account_number", text="Account Number")
        table.heading("name", text="Account Holder")
        table.heading("account_type", text="Account Type")
        table.heading("balance", text="Balance")

        table.column("account_number", width=150)
        table.column("name", width=230)
        table.column("account_type", width=150)
        table.column("balance", width=160)

        scrollbar = ttk.Scrollbar(
            parent,
            orient="vertical",
            command=table.yview
        )

        table.configure(yscrollcommand=scrollbar.set)

        table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for account in self.data["accounts"]:
            table.insert(
                "",
                "end",
                values=(
                    account.get("account_number", ""),
                    account.get("name", ""),
                    account.get("account_type", ""),
                    f"PHP {float(account.get('balance', 0)):,.2f}"
                )
            )

        return table

    # View all accounts
    def show_accounts(self):
        self.clear_main_area()
        self.data = load_data()

        self.create_header(
            "Bank Accounts",
            "View and manage registered bank accounts."
        )

        toolbar = tk.Frame(self.main_area, bg="#F3F4F6")
        toolbar.pack(fill="x", padx=30, pady=10)

        tk.Button(
            toolbar,
            text="+ Add New Account",
            bg="#2563EB",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=15,
            pady=9,
            command=self.add_account
        ).pack(side="left")

        tk.Button(
            toolbar,
            text="Search Account",
            bg="#059669",
            fg="white",
            font=("Arial", 10),
            relief="flat",
            padx=15,
            pady=9,
            command=self.search_account
        ).pack(side="left", padx=10)

        table_frame = tk.Frame(self.main_area, bg="#F3F4F6")
        table_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=15
        )

        self.create_account_table(table_frame, height=15)

    # Add account window
    def add_account(self):
        window = tk.Toplevel(self.root)
        window.title("Add Bank Account")
        window.geometry("400x430")
        window.resizable(False, False)
        window.configure(bg="white")
        window.transient(self.root)
        window.grab_set()

        tk.Label(
            window,
            text="CREATE BANK ACCOUNT",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#172554"
        ).pack(pady=20)

        fields = {}

        for label in (
            "Account Number",
            "Account Holder Name",
            "Username",
            "Initial Balance"
        ):
            tk.Label(
                window,
                text=label,
                bg="white",
                fg="#374151",
                font=("Arial", 10)
            ).pack(anchor="w", padx=35, pady=(7, 2))

            entry = tk.Entry(
                window,
                font=("Arial", 11),
                relief="solid",
                bd=1
            )
            entry.pack(fill="x", padx=35, ipady=6)
            fields[label] = entry

        tk.Label(
            window,
            text="Account Type",
            bg="white",
            fg="#374151",
            font=("Arial", 10)
        ).pack(anchor="w", padx=35, pady=(10, 2))

        account_type = ttk.Combobox(
            window,
            values=("Savings", "Checking", "Current"),
            state="readonly",
            font=("Arial", 10)
        )
        account_type.pack(fill="x", padx=35, ipady=4)
        account_type.set("Savings")

        def save_account():
            number = fields["Account Number"].get().strip()
            name = fields["Account Holder Name"].get().strip()
            username = fields["Username"].get().strip()

            try:
                balance = float(fields["Initial Balance"].get())

                if balance < 0:
                    raise ValueError

            except ValueError:
                messagebox.showerror(
                    "Invalid Balance",
                    "Enter a valid balance of zero or greater.",
                    parent=window
                )
                return

            if not number or not name or not username:
                messagebox.showerror(
                    "Missing Information",
                    "Please complete all fields.",
                    parent=window
                )
                return

            if "|" in number or "|" in name or "|" in username:
                messagebox.showerror(
                    "Invalid Information",
                    "The | character is not allowed.",
                    parent=window
                )
                return

            self.data = load_data()

            if any(
                account["account_number"] == number
                for account in self.data["accounts"]
            ):
                messagebox.showerror(
                    "Duplicate Account",
                    "Account number already exists.",
                    parent=window
                )
                return

            if not any(
                user.get("username") == username
                and user.get("role") == "user"
                for user in self.data["users"]
            ):
                messagebox.showerror(
                    "Customer Not Found",
                    "Create the customer's login account first.",
                    parent=window
                )
                return

            new_account = {
                "account_number": number,
                "username": username,
                "name": name,
                "account_type": account_type.get(),
                "balance": balance
            }

            self.data["accounts"].append(new_account)

            if save_data(self.data):
                messagebox.showinfo(
                    "Success",
                    "Bank account created successfully!",
                    parent=window
                )
                window.destroy()
                self.show_accounts()

        tk.Button(
            window,
            text="SAVE ACCOUNT",
            bg="#2563EB",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            command=save_account
        ).pack(fill="x", padx=35, pady=20, ipady=8)

    # Search account
    def search_account(self):
        self.data = load_data()

        window = tk.Toplevel(self.root)
        window.title("Search Account")
        window.geometry("380x180")
        window.configure(bg="white")
        window.transient(self.root)
        window.grab_set()

        tk.Label(
            window,
            text="Enter Account Number",
            font=("Arial", 12),
            bg="white"
        ).pack(pady=(25, 10))

        entry = tk.Entry(window, font=("Arial", 12))
        entry.pack(padx=30, fill="x")

        def find_account():
            number = entry.get().strip()

            for account in self.data["accounts"]:
                if account["account_number"] == number:
                    messagebox.showinfo(
                        "Account Found",
                        f"Account Number: {number}\n"
                        f"Account Holder: {account['name']}\n"
                        f"Account Type: {account['account_type']}\n"
                        f"Balance: PHP {account['balance']:,.2f}",
                        parent=window
                    )
                    return

            messagebox.showwarning(
                "Not Found",
                "Account does not exist.",
                parent=window
            )

        tk.Button(
            window,
            text="SEARCH",
            bg="#059669",
            fg="white",
            relief="flat",
            command=find_account
        ).pack(pady=15)

    # Customer information
    def show_customers(self):
        self.clear_main_area()
        self.data = load_data()

        self.create_header(
            "Customer Information",
            "View registered customer login accounts."
        )

        frame = tk.Frame(self.main_area, bg="#F3F4F6")
        frame.pack(fill="both", expand=True, padx=30, pady=15)

        columns = ("username", "fullname", "role")

        table = ttk.Treeview(
            frame,
            columns=columns,
            show="headings",
            height=15
        )

        table.heading("username", text="Username")
        table.heading("fullname", text="Full Name")
        table.heading("role", text="Role")

        table.column("username", width=180)
        table.column("fullname", width=250)
        table.column("role", width=150)

        for user in self.data["users"]:
            if user.get("role") == "user":
                table.insert(
                    "",
                    "end",
                    values=(
                        user.get("username", ""),
                        user.get("fullname", ""),
                        user.get("role", "")
                    )
                )

        table.pack(fill="both", expand=True)

    # Transaction history
    def show_transactions(self):
        self.clear_main_area()
        self.data = load_data()

        self.create_header(
            "Transaction History",
            "View recorded banking transactions."
        )

        frame = tk.Frame(self.main_area, bg="#F3F4F6")
        frame.pack(fill="both", expand=True, padx=30, pady=15)

        columns = (
            "date",
            "type",
            "account",
            "amount",
            "details"
        )

        table = ttk.Treeview(
            frame,
            columns=columns,
            show="headings",
            height=15
        )

        headings = {
            "date": "Date",
            "type": "Transaction Type",
            "account": "Account Number",
            "amount": "Amount",
            "details": "Details"
        }

        for column, heading in headings.items():
            table.heading(column, text=heading)
            table.column(column, width=130)

        for transaction in reversed(self.data["transactions"]):
            table.insert(
                "",
                "end",
                values=(
                    transaction.get("date", ""),
                    transaction.get("type", ""),
                    transaction.get("account_number", ""),
                    f"PHP {float(transaction.get('amount', 0)):,.2f}",
                    transaction.get("details", "")
                )
            )

        table.pack(fill="both", expand=True)

        if not self.data["transactions"]:
            tk.Label(
                frame,
                text="No transactions recorded yet.",
                bg="#F3F4F6",
                fg="#6B7280",
                font=("Arial", 11)
            ).pack(pady=10)

    # Refresh information
    def refresh_data(self):
        self.data = load_data()
        self.show_dashboard()

        messagebox.showinfo(
            "Refresh",
            "Dashboard information has been refreshed."
        )

    # Exit program
    def exit_program(self):
        if messagebox.askyesno(
            "Exit LocBank",
            "Are you sure you want to close the Staff GUI?"
        ):
            self.root.destroy()


# Run Staff GUI independently
if __name__ == "__main__":
    root = tk.Tk()
    app = StaffGUI(root)
    root.mainloop()
