import unittest
from functools import reduce
from besttrade.src.domain import Account
from besttrade.tests.db.SqlLite3Connector import SqlLite3Connector
from besttrade.src.db import DataAccessObject


class TestGetAccounts(unittest.TestCase):

    def setUp(self) -> None:
        dao = DataAccessObject(SqlLite3Connector())
        cnx = dao.get_connection()
        scripts_path = './besttrade/tests/resources'
        with open(f'{scripts_path}/create_db_objects.sql', 'r') as f:
            cnx.executescript(f.read())
        with open(f'{scripts_path}/populate_db.sql', 'r') as f:
            cnx.executescript(f.read())
        cnx.commit()
        cnx.close()

    def test_get_all_accounts(self):
        dao = DataAccessObject(SqlLite3Connector())
        accounts = dao.get_all_accounts()
        self.assertIsNotNone(accounts)
        self.assertFalse(len(accounts) == 0)
        self.assertEqual(3, len(accounts))
        self.assertEqual(27000, reduce(lambda x, y: x + y,
                         [account.balance for account in accounts]))
        self.assertTrue(all(account.account_number in [
                        1, 2, 3] for account in accounts))

    def test_get_account_by_id(self):
        dao = DataAccessObject(SqlLite3Connector())
        account = dao.get_account_by_id(1)
        self.assertIsNotNone(account)
        self.assertEqual(1, account.account_number)
        self.assertEqual(1, account.investor_id)
        self.assertEqual(10000, account.balance)

    def test_get_account_by_invalid_id(self):
        dao = DataAccessObject(SqlLite3Connector())
        account = dao.get_account_by_id(-9999)
        self.assertIsNone(account)

    def test_get_accounts_by_investor_id(self):
        dao = DataAccessObject(SqlLite3Connector())
        accounts = dao.get_account_by_investor_id(1)
        self.assertIsNotNone(accounts)
        self.assertFalse(len(accounts) == 0)
        self.assertEqual(2, len(accounts))
        investors_ids = {account.investor_id for account in accounts}
        self.assertEqual(1, len(investors_ids))
        self.assertEqual(15000, reduce(lambda x, y: x + y,
                         [account.balance for account in accounts]))

    def test_get_accounts_for_invalid_investor(self):
        dao = DataAccessObject(SqlLite3Connector())
        accounts = dao.get_account_by_id(-9999)
        self.assertIsNone(accounts)

    def test_create_account(self):
        dao = DataAccessObject(SqlLite3Connector())
        # before creating new account
        accounts = dao.get_account_by_investor_id(1)
        self.assertIsNotNone(accounts)
        self.assertFalse(len(accounts) == 0)
        self.assertEqual(2, len(accounts))
        self.assertEqual(15000, reduce(lambda x, y: x + y,
                         [account.balance for account in accounts]))
        # add one more account
        highest_acct_number = dao.get_connection().execute(
            'select max(account_number) from account').fetchone()[0]
        expected_acct_number = highest_acct_number + 1
        account = dao.create_account(1, 2000)
        self.assertIsNotNone(account)
        self.assertEqual(1, account.investor_id)
        self.assertEqual(expected_acct_number, account.account_number)
        accounts = dao.get_account_by_investor_id(1)
        self.assertEqual(17000, reduce(lambda x, y: x + y,
                         [account.balance for account in accounts]))

    def test_delete_account(self):
        dao = DataAccessObject(SqlLite3Connector())
        # before deleting account
        accounts = dao.get_all_accounts()
        self.assertIsNotNone(accounts)
        self.assertFalse(len(accounts) == 0)
        self.assertEqual(3, len(accounts))
        # delete account with ID 3
        dao.delete_account(3)
        accounts = dao.get_all_accounts()
        self.assertIsNotNone(accounts)
        self.assertFalse(len(accounts) == 0)
        self.assertEqual(2, len(accounts))

    def test_update_account_balance(self):
        dao = DataAccessObject(SqlLite3Connector())
        # before update
        accounts = dao.get_account_by_investor_id(1)
        self.assertIsNotNone(accounts)
        self.assertFalse(len(accounts) == 0)
        self.assertEqual(2, len(accounts))
        self.assertEqual(15000, reduce(lambda x, y: x + y,
                         [account.balance for account in accounts]))
        # update balance for account with ID 2
        dao.update_account_balance(2, 2000)
        accounts = dao.get_account_by_investor_id(1)
        self.assertIsNotNone(accounts)
        self.assertTrue(2, len(accounts))
        self.assertEqual(12000, reduce(lambda x, y: x + y,
                         [account.balance for account in accounts]))
