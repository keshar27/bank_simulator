"""
history_manager.py
Module 3: History, Reporting & Statements

Logs every transaction to a CSV file and provides mini-statement and
bank-wide reporting functions on top of that log.
"""

import csv
import os
from datetime import datetime

HISTORY_FILE = os.path.join(os.path.dirname(__file__), "data", "transactions.csv")
FIELDNAMES = ["timestamp", "account_no", "type", "amount", "balance_after"]


def _ensure_file():
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def log_transaction(account_no, txn_type, amount, balance_after):
    """Appends one transaction record to the CSV log."""
    _ensure_file()
    with open(HISTORY_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "account_no": account_no,
            "type": txn_type,
            "amount": f"{amount:.2f}",
            "balance_after": f"{balance_after:.2f}",
        })


def read_all_transactions():
    """Returns all transaction records as a list of dicts, newest first."""
    _ensure_file()
    with open(HISTORY_FILE, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        records = list(reader)
    return list(reversed(records))


def mini_statement(account_no, limit=10):
    """Returns the most recent `limit` transactions for a specific account."""
    all_txns = read_all_transactions()
    account_txns = [t for t in all_txns if t["account_no"] == account_no]
    return account_txns[:limit]


def total_transactions_count():
    return len(read_all_transactions())


def transactions_by_type():
    """Returns a dict counting how many transactions of each type occurred."""
    counts = {}
    for t in read_all_transactions():
        counts[t["type"]] = counts.get(t["type"], 0) + 1
    return counts


def total_deposits_and_withdrawals():
    """Returns (total_deposited, total_withdrawn) across the whole bank."""
    total_deposit = 0.0
    total_withdraw = 0.0
    for t in read_all_transactions():
        amount = float(t["amount"])
        if t["type"] == "DEPOSIT":
            total_deposit += amount
        elif t["type"] == "WITHDRAW":
            total_withdraw += amount
    return round(total_deposit, 2), round(total_withdraw, 2)


def export_bank_report(accounts, output_path=None):
    """
    Exports a full bank summary report: all active accounts with balances,
    plus transaction statistics. `accounts` is the list from
    account_manager.all_active_accounts().
    """
    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), "data", "bank_report.txt")

    total_deposit, total_withdraw = total_deposits_and_withdrawals()
    txn_counts = transactions_by_type()
    total_balance = sum(acc["balance"] for acc in accounts)

    with open(output_path, mode="w", encoding="utf-8") as f:
        f.write("BankSim - Bank Summary Report\n")
        f.write("=" * 45 + "\n")
        f.write(f"Total active accounts: {len(accounts)}\n")
        f.write(f"Total balance across bank: {total_balance:,.2f}\n")
        f.write(f"Total deposited (all time): {total_deposit:,.2f}\n")
        f.write(f"Total withdrawn (all time): {total_withdraw:,.2f}\n")
        f.write(f"Transaction counts by type: {txn_counts}\n")
        f.write("\nAccount List:\n")
        f.write("-" * 45 + "\n")
        for acc in sorted(accounts, key=lambda a: a["balance"], reverse=True):
            f.write(f"{acc['account_no']} | {acc['name']} | {acc['account_type']} "
                     f"| Balance: {acc['balance']:,.2f}\n")

    return output_path
