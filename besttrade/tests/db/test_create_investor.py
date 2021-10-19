import unittest
from besttrade.tests.db.SqlLite3Connector import SqlLite3Connector
from besttrade.src.db import DataAccessObject


class TestCreateInvestor(unittest.TestCase):
    def setUp(self) -> None:
        dao = DataAccessObject(SqlLite3Connector())
        cnx = dao.get_connection()
        scripts_path = './besttrade/tests/resources'
        with open(f'{scripts_path}/create_db_objects.sql', 'r') as f:
            cnx.executescript(f.read())
        with open(f'{scripts_path}/populate_db.sql', 'r') as f:
            cnx.executescript(f.read())
        cnx.close()

    def test_create_investor(self):
        dao = DataAccessObject(SqlLite3Connector())
        # before creating new investor
        investors = dao.get_active_investors()
        self.assertEqual(3, len(investors))
        # add new investor
        new_investor = dao.create_investor('user3')
        investors = dao.get_active_investors()
        self.assertEqual(4, len(investors))
        self.assertIsNotNone(new_investor)
        self.assertEqual('user3', new_investor.username)
        self.assertEqual('ACTIVE', new_investor.status)
