"""
transaction_manager.py
Module 2: Transactions

Handles deposits, withdrawals, transfers, and interest computation.
Every successful transaction is logged via history_manager (Module 3).
Business rules (minimum balance, withdrawal limits) are enforced here.

Business rules:
- Savings accounts must maintain a minimum balance of 500.
- Current accounts have no minimum balance requirement.
- A single withdrawal cannot exceed 100,000.
- Savings accounts earn interest; current accounts do not.
"""

import account_manager as am
import history_manager as hm

MIN_SAVINGS_BALANCE = 500.0
MAX_WITHDRAWAL = 100000.0
SAVINGS_INTEREST_RATE = 0.035  # 3.5% annual, applied as a simple flat-rate demo


def deposit(account_no, amount):
    """Deposits `amount` into the account. Returns the new balance."""
    if amount <= 0:
        raise ValueError("Deposit amount must be positive.")
    account = am.get_account(account_no)
    if account is None or account["status"] != "active":
        raise ValueError("Account not found or inactive.")

    new_balance = account["balance"] + amount
    am.update_balance(account_no, new_balance)
    hm.log_transaction(account_no, "DEPOSIT", amount, new_balance)
    return new_balance


def withdraw(account_no, amount):
    """Withdraws `amount` from the account, enforcing minimum balance and limits."""
    if amount <= 0:
        raise ValueError("Withdrawal amount must be positive.")
    if amount > MAX_WITHDRAWAL:
        raise ValueError(f"Cannot withdraw more than {MAX_WITHDRAWAL:,.2f} in a single transaction.")

    account = am.get_account(account_no)
    if account is None or account["status"] != "active":
        raise ValueError("Account not found or inactive.")

    new_balance = account["balance"] - amount

    if account["account_type"] == "savings" and new_balance < MIN_SAVINGS_BALANCE:
        raise ValueError(
            f"Insufficient funds. Savings accounts must maintain a minimum "
            f"balance of {MIN_SAVINGS_BALANCE:,.2f}."
        )
    if new_balance < 0:
        raise ValueError("Insufficient funds.")

    am.update_balance(account_no, new_balance)
    hm.log_transaction(account_no, "WITHDRAW", amount, new_balance)
    return new_balance


def transfer(from_account_no, to_account_no, amount):
    """
    Transfers `amount` from one account to another. Performs the withdrawal
    first (validating funds/minimum balance), then the deposit. If the
    deposit step were to fail, the withdrawal is rolled back.
    """
    if from_account_no == to_account_no:
        raise ValueError("Cannot transfer to the same account.")
    if not am.account_exists(to_account_no):
        raise ValueError("Destination account not found or inactive.")

    new_from_balance = withdraw(from_account_no, amount)

    try:
        new_to_balance = deposit(to_account_no, amount)
    except ValueError:
        # Roll back the withdrawal if the deposit somehow fails
        rollback_balance = am.get_account(from_account_no)["balance"] + amount
        am.update_balance(from_account_no, rollback_balance)
        raise

    return new_from_balance, new_to_balance


def apply_interest(account_no):
    """
    Applies a flat annual interest rate to a savings account balance.
    Raises ValueError if the account is not a savings account.
    """
    account = am.get_account(account_no)
    if account is None or account["status"] != "active":
        raise ValueError("Account not found or inactive.")
    if account["account_type"] != "savings":
        raise ValueError("Interest can only be applied to savings accounts.")

    interest = round(account["balance"] * SAVINGS_INTEREST_RATE, 2)
    new_balance = account["balance"] + interest
    am.update_balance(account_no, new_balance)
    hm.log_transaction(account_no, "INTEREST", interest, new_balance)
    return interest, new_balance


def apply_interest_to_all_savings():
    """Applies interest to every active savings account. Returns a summary list."""
    results = []
    for account in am.all_active_accounts():
        if account["account_type"] == "savings":
            interest, new_balance = apply_interest(account["account_no"])
            results.append((account["account_no"], interest, new_balance))
    return results
