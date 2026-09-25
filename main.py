"""
main.py
BankSim - Console-Based Bank Account Management System
Entry point that ties together Module 1 (account_manager),
Module 2 (transaction_manager), and Module 3 (history_manager).

Run with:
    python main.py
"""

import account_manager as am
import transaction_manager as tm
import history_manager as hm
from utils import get_float, get_nonempty_str, get_choice, format_currency, pause, print_header


def account_menu():
    print_header("MODULE 1: Account Management")
    print("1. Open New Account")
    print("2. View Account Details")
    print("3. Search Accounts by Name")
    print("4. List All Active Accounts")
    print("5. Close Account")
    print("0. Back to Main Menu")

    choice = input("\nEnter your choice: ").strip()

    try:
        if choice == "1":
            name = get_nonempty_str("Enter account holder name: ")
            acc_type = get_choice("Account type (savings/current): ", ["savings", "current"])
            opening_balance = get_float("Enter opening balance: ")
            account_no = am.create_account(name, acc_type, opening_balance)
            print(f"\nAccount created successfully! Account Number: {account_no}")

        elif choice == "2":
            account_no = get_nonempty_str("Enter account number: ").upper()
            account = am.get_account(account_no)
            if account is None:
                print("\nAccount not found.")
            else:
                print(f"\nAccount No : {account['account_no']}")
                print(f"Name       : {account['name']}")
                print(f"Type       : {account['account_type']}")
                print(f"Balance    : {format_currency(account['balance'])}")
                print(f"Opened On  : {account['created_on']}")
                print(f"Status     : {account['status']}")

        elif choice == "3":
            keyword = get_nonempty_str("Enter name to search: ")
            results = am.search_by_name(keyword)
            if not results:
                print("\nNo matching accounts found.")
            else:
                for acc in results:
                    print(f"  {acc['account_no']} | {acc['name']} | "
                          f"{format_currency(float(acc['balance']))} | {acc['status']}")

        elif choice == "4":
            accounts = am.all_active_accounts()
            if not accounts:
                print("\nNo active accounts yet.")
            else:
                print(f"\n{'Acc No':<10}{'Name':<20}{'Type':<10}{'Balance':>12}")
                print("-" * 52)
                for acc in accounts:
                    print(f"{acc['account_no']:<10}{acc['name']:<20}{acc['account_type']:<10}"
                          f"{format_currency(float(acc['balance'])):>12}")

        elif choice == "5":
            account_no = get_nonempty_str("Enter account number to close: ").upper()
            am.close_account(account_no)
            print(f"\nAccount {account_no} closed successfully.")

        elif choice == "0":
            return
        else:
            print("\nInvalid choice.")

    except ValueError as e:
        print(f"\nError: {e}")

    pause()


def transaction_menu():
    print_header("MODULE 2: Transactions")
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Transfer Between Accounts")
    print("4. Apply Interest (single savings account)")
    print("5. Apply Interest to All Savings Accounts")
    print("0. Back to Main Menu")

    choice = input("\nEnter your choice: ").strip()

    try:
        if choice == "1":
            account_no = get_nonempty_str("Enter account number: ").upper()
            amount = get_float("Enter deposit amount: ", allow_zero=False)
            new_balance = tm.deposit(account_no, amount)
            print(f"\nDeposit successful. New balance: {format_currency(new_balance)}")

        elif choice == "2":
            account_no = get_nonempty_str("Enter account number: ").upper()
            amount = get_float("Enter withdrawal amount: ", allow_zero=False)
            new_balance = tm.withdraw(account_no, amount)
            print(f"\nWithdrawal successful. New balance: {format_currency(new_balance)}")

        elif choice == "3":
            from_acc = get_nonempty_str("From account number: ").upper()
            to_acc = get_nonempty_str("To account number: ").upper()
            amount = get_float("Enter transfer amount: ", allow_zero=False)
            new_from, new_to = tm.transfer(from_acc, to_acc, amount)
            print(f"\nTransfer successful.")
            print(f"  {from_acc} new balance: {format_currency(new_from)}")
            print(f"  {to_acc} new balance: {format_currency(new_to)}")

        elif choice == "4":
            account_no = get_nonempty_str("Enter savings account number: ").upper()
            interest, new_balance = tm.apply_interest(account_no)
            print(f"\nInterest applied: {format_currency(interest)}")
            print(f"New balance: {format_currency(new_balance)}")

        elif choice == "5":
            results = tm.apply_interest_to_all_savings()
            if not results:
                print("\nNo active savings accounts found.")
            else:
                print(f"\nInterest applied to {len(results)} savings account(s):")
                for acc_no, interest, new_balance in results:
                    print(f"  {acc_no}: +{format_currency(interest)} -> {format_currency(new_balance)}")

        elif choice == "0":
            return
        else:
            print("\nInvalid choice.")

    except ValueError as e:
        print(f"\nError: {e}")

    pause()


def report_menu():
    print_header("MODULE 3: History & Reporting")
    print("1. Mini Statement (single account)")
    print("2. Bank-Wide Transaction Statistics")
    print("3. Export Full Bank Report")
    print("0. Back to Main Menu")

    choice = input("\nEnter your choice: ").strip()

    if choice == "1":
        account_no = get_nonempty_str("Enter account number: ").upper()
        txns = hm.mini_statement(account_no)
        if not txns:
            print("\nNo transactions found for this account.")
        else:
            print(f"\nLast {len(txns)} transactions for {account_no}:")
            for t in txns:
                print(f"  [{t['timestamp']}] {t['type']:<10} "
                      f"Amount: {format_currency(float(t['amount']))}  "
                      f"Balance After: {format_currency(float(t['balance_after']))}")

    elif choice == "2":
        total = hm.total_transactions_count()
        counts = hm.transactions_by_type()
        total_deposit, total_withdraw = hm.total_deposits_and_withdrawals()
        print(f"\nTotal transactions recorded: {total}")
        print(f"By type: {counts}")
        print(f"Total deposited (all time): {format_currency(total_deposit)}")
        print(f"Total withdrawn (all time): {format_currency(total_withdraw)}")

    elif choice == "3":
        accounts = am.all_active_accounts()
        path = hm.export_bank_report(accounts)
        print(f"\nReport exported to: {path}")

    elif choice == "0":
        return
    else:
        print("\nInvalid choice.")

    pause()


def main_menu():
    am.load_accounts()  # Load existing accounts from disk at startup

    while True:
        print_header("BANKSIM - MAIN MENU")
        print("1. Account Management")
        print("2. Transactions")
        print("3. History & Reporting")
        print("4. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            account_menu()
        elif choice == "2":
            transaction_menu()
        elif choice == "3":
            report_menu()
        elif choice == "4":
            print("\nThank you for using BankSim. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")
            pause()


if __name__ == "__main__":
    main_menu()
