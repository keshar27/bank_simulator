"""
account_manager.py
Module 1: Account Management

Stores all accounts in memory as a dictionary keyed by account number,
and persists them to a CSV file so data survives between runs.
Each account is itself a dictionary with: account_no, name, balance,
account_type, created_on.
"""

import csv
import os
from datetime import datetime

ACCOUNTS_FILE = os.path.join(os.path.dirname(__file__), "data", "accounts.csv")
FIELDNAMES = ["account_no", "name", "account_type", "balance", "created_on", "status"]

# In-memory store: {account_no: {..account fields..}}
_accounts = {}


def _ensure_file():
    os.makedirs(os.path.dirname(ACCOUNTS_FILE), exist_ok=True)
    if not os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def load_accounts():
    """Loads all accounts from the CSV file into memory. Call once at startup."""
    global _accounts
    _ensure_file()
    _accounts = {}
    with open(ACCOUNTS_FILE, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["balance"] = float(row["balance"])
            _accounts[row["account_no"]] = row
    return _accounts


def save_accounts():
    """Writes the full in-memory account dictionary back to the CSV file."""
    _ensure_file()
    with open(ACCOUNTS_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for account in _accounts.values():
            writer.writerow(account)


def _generate_account_no():
    """Generates a new sequential account number like ACC1001, ACC1002, ..."""
    if not _accounts:
        return "ACC1001"
    max_num = max(int(acc_no.replace("ACC", "")) for acc_no in _accounts.keys())
    return f"ACC{max_num + 1}"


def create_account(name, account_type, opening_balance):
    """Creates a new account and returns its account number."""
    if opening_balance < 0:
        raise ValueError("Opening balance cannot be negative.")
    if account_type.lower() not in ("savings", "current"):
        raise ValueError("Account type must be 'savings' or 'current'.")

    account_no = _generate_account_no()
    _accounts[account_no] = {
        "account_no": account_no,
        "name": name,
        "account_type": account_type.lower(),
        "balance": round(opening_balance, 2),
        "created_on": datetime.now().strftime("%Y-%m-%d"),
        "status": "active",
    }
    save_accounts()
    return account_no


def get_account(account_no):
    """Returns the account dict for a given account number, or None if not found."""
    return _accounts.get(account_no)


def account_exists(account_no):
    return account_no in _accounts and _accounts[account_no]["status"] == "active"


def search_by_name(name_keyword):
    """Returns a list of accounts whose holder name contains the given keyword."""
    keyword = name_keyword.lower()
    return [acc for acc in _accounts.values() if keyword in acc["name"].lower()]


def close_account(account_no):
    """Marks an account as closed. Raises ValueError if balance is not zero."""
    account = get_account(account_no)
    if account is None:
        raise ValueError("Account not found.")
    if account["status"] != "active":
        raise ValueError("Account is already closed.")
    if account["balance"] > 0:
        raise ValueError(
            f"Cannot close account with a non-zero balance "
            f"(current balance: {account['balance']}). Please withdraw first."
        )
    account["status"] = "closed"
    save_accounts()


def all_active_accounts():
    """Returns a list of all accounts with status 'active'."""
    return [acc for acc in _accounts.values() if acc["status"] == "active"]


def update_balance(account_no, new_balance):
    """Directly sets an account's balance and persists it. Used by transaction_manager."""
    account = get_account(account_no)
    if account is None:
        raise ValueError("Account not found.")
    account["balance"] = round(new_balance, 2)
    save_accounts()
