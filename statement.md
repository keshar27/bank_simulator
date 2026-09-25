# Problem Statement

Manual bookkeeping of bank account transactions is error-prone and time
consuming — tracking balances, ensuring minimum-balance rules are followed,
and reviewing transaction history all become difficult without an automated
system. There is a need for a lightweight application that models these
banking operations while enforcing correct financial rules.

## Scope of the Project
BankSim is a console-based, single-user, offline banking simulation. It
models a real-world entity — a bank and its customer accounts — using core
programming constructs (functions, dictionaries, conditionals, loops, and
file I/O) taught in CSE1021. It does not include multi-user authentication,
network access, or a graphical interface; those are noted as future
enhancements.

## Target Users
- Students learning to model real-world entities and enforce business rules
  through code.
- Anyone wanting a simple, dependency-free tool to simulate basic banking
  operations for learning or demonstration purposes.

## High-Level Features
1. **Account Management Module** — create savings/current accounts, view
   and search account details, list all active accounts, and close accounts
   once their balance reaches zero.
2. **Transaction Module** — deposit, withdraw, and transfer funds between
   accounts, with minimum-balance and withdrawal-limit rules enforced;
   interest calculation for savings accounts.
3. **History & Reporting Module** — per-account mini-statements, bank-wide
   transaction statistics, and an exportable summary report of all accounts
   and their balances.

Each module is implemented in its own file, validates its inputs, enforces
its business rules through conditional logic, and is covered by an
automated unit test suite.
