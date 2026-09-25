"""
test_bank.py
Unit tests for account_manager.py and transaction_manager.py.

Uses a temporary/isolated data directory so tests never touch real
account or transaction data.

Run with:
    python -m unittest tests/test_bank.py
"""

import unittest
import sys
import os
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import account_manager as am
import transaction_manager as tm
import history_manager as hm


class TestBankSim(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Redirect all file storage to a temporary test folder so we never
        # touch real application data.
        test_dir = os.path.join(os.path.dirname(__file__), "_test_data")
        os.makedirs(test_dir, exist_ok=True)
        am.ACCOUNTS_FILE = os.path.join(test_dir, "accounts.csv")
        hm.HISTORY_FILE = os.path.join(test_dir, "transactions.csv")
        cls.test_dir = test_dir

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.test_dir, ignore_errors=True)

    def setUp(self):
        # Reset in-memory state and files before every test
        if os.path.exists(am.ACCOUNTS_FILE):
            os.remove(am.ACCOUNTS_FILE)
        if os.path.exists(hm.HISTORY_FILE):
            os.remove(hm.HISTORY_FILE)
        am.load_accounts()

    def test_create_account(self):
        acc_no = am.create_account("Alice", "savings", 1000)
        self.assertTrue(am.account_exists(acc_no))
        account = am.get_account(acc_no)
        self.assertEqual(account["name"], "Alice")
        self.assertEqual(account["balance"], 1000)

    def test_create_account_invalid_type(self):
        with self.assertRaises(ValueError):
            am.create_account("Bob", "crypto", 500)

    def test_deposit(self):
        acc_no = am.create_account("Carol", "current", 500)
        new_balance = tm.deposit(acc_no, 250)
        self.assertEqual(new_balance, 750)

    def test_withdraw_success(self):
        acc_no = am.create_account("Dave", "current", 1000)
        new_balance = tm.withdraw(acc_no, 300)
        self.assertEqual(new_balance, 700)

    def test_withdraw_below_minimum_savings(self):
        acc_no = am.create_account("Eve", "savings", 1000)
        with self.assertRaises(ValueError):
            tm.withdraw(acc_no, 900)  # would leave balance below 500 minimum

    def test_withdraw_exceeds_limit(self):
        acc_no = am.create_account("Frank", "current", 200000)
        with self.assertRaises(ValueError):
            tm.withdraw(acc_no, 150000)  # exceeds MAX_WITHDRAWAL

    def test_transfer(self):
        acc1 = am.create_account("Grace", "current", 1000)
        acc2 = am.create_account("Heidi", "current", 200)
        new_from, new_to = tm.transfer(acc1, acc2, 300)
        self.assertEqual(new_from, 700)
        self.assertEqual(new_to, 500)

    def test_transfer_same_account_fails(self):
        acc1 = am.create_account("Ivan", "current", 1000)
        with self.assertRaises(ValueError):
            tm.transfer(acc1, acc1, 100)

    def test_apply_interest_savings_only(self):
        acc_no = am.create_account("Judy", "savings", 1000)
        interest, new_balance = tm.apply_interest(acc_no)
        self.assertAlmostEqual(interest, 35.0, places=2)  # 3.5% of 1000
        self.assertAlmostEqual(new_balance, 1035.0, places=2)

    def test_apply_interest_current_fails(self):
        acc_no = am.create_account("Karl", "current", 1000)
        with self.assertRaises(ValueError):
            tm.apply_interest(acc_no)

    def test_close_account_with_balance_fails(self):
        acc_no = am.create_account("Liam", "current", 500)
        with self.assertRaises(ValueError):
            am.close_account(acc_no)

    def test_close_account_zero_balance(self):
        acc_no = am.create_account("Mia", "current", 0)
        am.close_account(acc_no)
        self.assertFalse(am.account_exists(acc_no))

    def test_search_by_name(self):
        am.create_account("Nora Smith", "savings", 100)
        am.create_account("Oscar Smith", "current", 200)
        am.create_account("Paul Jones", "savings", 300)
        results = am.search_by_name("smith")
        self.assertEqual(len(results), 2)

    def test_mini_statement_logs_transactions(self):
        acc_no = am.create_account("Quinn", "current", 500)
        tm.deposit(acc_no, 100)
        tm.withdraw(acc_no, 50)
        statement = hm.mini_statement(acc_no)
        self.assertEqual(len(statement), 2)


if __name__ == "__main__":
    unittest.main()
