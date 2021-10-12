import unittest
from besttrade.tests.db.SqlLite3Connector import SqlLite3Connector
from besttrade.src.db import DataAccessObject


class TestGetAllInvestors(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        dao = DataAccessObject(SqlLite3Connector())
        cnx = dao.get_connection()
        scripts_path = './besttrade/tests/resources'
        with open(f'{scripts_path}/create_db_objects.sql', 'r') as f:
            cnx.executescript(f.read())
        with open(f'{scripts_path}/populate_investor.sql', 'r') as f:
            cnx.executescript(f.read())
        cnx.close()

    def test_get_all_active_investors(self):
        dao = DataAccessObject(SqlLite3Connector())
        investors = dao.get_active_investors()
        self.assertIsNotNone(investors)
        self.assertTrue(isinstance(investors, list))
        self.assertFalse(len(investors) == 0)
        self.assertEqual(2, len(investors))
        investor_names = [investor.username for investor in investors]
        self.assertTrue(
            all(investor in investor_names for investor in ['admin', 'user1']))

    def test_get_all_investors(self):
        dao = DataAccessObject(SqlLite3Connector())
        investors = dao.get_investors()
        self.assertIsNotNone(investors)
        self.assertTrue(isinstance(investors, list))
        self.assertFalse(len(investors) == 0)
        self.assertEqual(3, len(investors))
        investor_names = [investor.username for investor in investors]
        self.assertTrue(
            all(investor in investor_names for investor in ['admin', 'user1', 'user2']))

    def test_get_investor_by_id(self):
        dao = DataAccessObject(SqlLite3Connector())
        investor = dao.get_investor_by_id(1)
        self.assertIsNotNone(investor)
        self.assertEqual(1, investor.id)
        self.assertEqual('admin', investor.username)
        self.assertEqual('ACTIVE', investor.status)
