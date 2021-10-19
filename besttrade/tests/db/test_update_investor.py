import unittest
from besttrade.tests.db.SqlLite3Connector import SqlLite3Connector
from besttrade.src.db import DataAccessObject
from besttrade.src.domain import Investor


class TestCreateInvestor(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        dao = DataAccessObject(SqlLite3Connector())
        cnx = dao.get_connection()
        scripts_path = './besttrade/tests/resources'
        with open(f'{scripts_path}/create_db_objects.sql', 'r') as f:
            cnx.executescript(f.read())
        with open(f'{scripts_path}/populate_db.sql', 'r') as f:
            cnx.executescript(f.read())
        cnx.close()

    def test_update_investor_status(self):
        dao = DataAccessObject(SqlLite3Connector())
        # before updating investor
        investors = dao.get_investors()
        self.assertTrue(
            'INACTIVE' in [investor.status for investor in investors])
        # update investor
        dao.update_investor_status(3, 'ACTIVE')
        investors = dao.get_investors()
        self.assertFalse(
            'INACTIVE' in [investor.status for investor in investors])

    def test_update_investor_name(self):
        dao = DataAccessObject(SqlLite3Connector())
        # before updating the name
        investor = dao.get_investor_by_id(1)
        self.assertIsNotNone(investor)
        self.assertTrue(isinstance(investor, Investor))
        self.assertEqual('admin', investor.username)
        # update investor name
        dao.update_investor_name(1, 'admin2')
        investor = dao.get_investor_by_id(1)
        self.assertIsNotNone(investor)
        self.assertTrue(isinstance(investor, Investor))
        self.assertEqual('admin2', investor.username)
