# BankSim — Console-Based Bank Account Management System

## Overview
BankSim is a console-based Python application that simulates core banking
operations: opening accounts, deposits, withdrawals, transfers, interest
calculation, and transaction reporting. Built as a course project for
**CSE1021 – Introduction to Problem Solving and Programming**, it applies
functions, conditionals, dictionaries, and file I/O to model a real-world
entity (a bank and its accounts).

## Features
- **Account Management**: open savings/current accounts, view account
  details, search accounts by holder name, list all active accounts, close
  accounts (only when balance is zero).
- **Transactions**: deposit, withdraw (with minimum-balance and per-transaction
  limit rules), transfer funds between accounts (with automatic rollback if
  a transfer step fails), and interest calculation for savings accounts
  (single account or bank-wide).
- **History & Reporting**: mini-statement per account, bank-wide transaction
  statistics (counts by type, total deposited/withdrawn), and a full
  exportable bank summary report.
- Persistent storage via CSV files — account and transaction data survive
  between runs.
- Input validation throughout so invalid amounts or account numbers never
  crash the program.

## Business Rules
- Savings accounts must maintain a minimum balance of **$500**.
- Current accounts have no minimum balance requirement.
- A single withdrawal cannot exceed **$100,000**.
- Only savings accounts earn interest (3.5% flat rate per application).
- An account can only be closed once its balance is exactly zero.

## Technologies / Tools Used
- Python 3 (standard library only — no external dependencies)
- `unittest` for automated testing
- CSV file storage for accounts and transaction history
- Git & GitHub for version control

## Project Structure
```
bank_simulator/
├── main.py                  # Menu-driven entry point
├── account_manager.py        # Module 1: account creation, search, closure
├── transaction_manager.py     # Module 2: deposit, withdraw, transfer, interest
├── history_manager.py         # Module 3: transaction logging and reporting
├── utils.py                   # Shared input validation helpers
├── tests/
│   └── test_bank.py           # Unit tests (isolated from real data)
├── data/
│   ├── accounts.csv           # Auto-generated account records
│   └── transactions.csv       # Auto-generated transaction log
├── README.md
└── statement.md
```

## Steps to Install & Run
1. Ensure Python 3.8+ is installed:
   ```
   python3 --version
   ```
2. Clone this repository:
   ```
   git clone <your-repo-url>
   cd bank_simulator
   ```
3. Run the program:
   ```
   python3 main.py
   ```
4. Use the menu to open an account, then try deposits, withdrawals, and
   transfers using the generated account number (e.g. `ACC1001`).

## Instructions for Testing
Run the full unit test suite from the project root:
```
python3 -m unittest tests/test_bank.py -v
```
Tests use an isolated temporary data folder, so they never touch your real
`data/accounts.csv` or `data/transactions.csv`. All 14 tests should pass,
covering account creation, deposits, withdrawals, transfers, interest rules,
and account closure edge cases.

## Screenshots
_(Add terminal screenshots of the main menu, account creation, and a
transaction here before submission.)_

## Future Enhancements
- Add PIN-based authentication per account
- Support fixed deposits with tenure and maturity calculation
- Add a loan/EMI calculator module
- Migrate storage from CSV to SQLite for larger datasets
