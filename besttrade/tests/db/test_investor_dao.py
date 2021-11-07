import unittest
from besttrade.src.db.InvestorDAO import InvestorDAO
from besttrade.src.domain import Investor
from besttrade.tests.db.SqlLite3Connector import SqlLite3Connector

class TestInvestorDAO(unittest.TestCase):
    def setUp(self) -> None:
        cnx = SqlLite3Connector().get_connection()
        scripts_path = './besttrade/tests/resources'
        with open(f'{scripts_path}/create_db_objects.sql', 'r') as f:
            cnx.executescript(f.read())
        with open(f'{scripts_path}/populate_db.sql', 'r') as f:
            cnx.executescript(f.read())
        cnx.commit()
        cnx.close()
    
    def test_get_investors(self):
        dao = InvestorDAO(SqlLite3Connector())
        investors = dao.get_investors()
        self.assertIsNotNone(investors)
        self.assertFalse(len(investors) == 0)
        self.assertEqual(3, len(investors))
        investor_names = [x.username for x in investors]
        self.assertIsNotNone(investor_names)
        self.assertFalse(len(investor_names) == 0)
        self.assertTrue(all(x in ['admin', 'user1', 'user2'] for x in investor_names))

    def test_get_all_active_investors(self):
        dao = InvestorDAO(SqlLite3Connector())
        investors = dao.get_active_investors()
        self.assertIsNotNone(investors)
        self.assertTrue(isinstance(investors, list))
        self.assertFalse(len(investors) == 0)
        self.assertEqual(2, len(investors))
        investor_names = [investor.username for investor in investors]
        self.assertTrue(
            all(investor in investor_names for investor in ['admin', 'user1']))

    def test_get_all_investors(self):
        dao = InvestorDAO(SqlLite3Connector())
        investors = dao.get_investors()
        self.assertIsNotNone(investors)
        self.assertTrue(isinstance(investors, list))
        self.assertFalse(len(investors) == 0)
        self.assertEqual(3, len(investors))
        investor_names = [investor.username for investor in investors]
        self.assertTrue(
            all(investor in investor_names for investor in ['admin', 'user1', 'user2']))

    def test_get_investor_by_id(self):
        dao = InvestorDAO(SqlLite3Connector())
        investor = dao.get_investor_by_id(1)
        self.assertIsNotNone(investor)
        self.assertEqual(1, investor.id)
        self.assertEqual('admin', investor.username)
        self.assertEqual('ACTIVE', investor.status)

    def test_get_investors_by_name(self):
        dao = InvestorDAO(SqlLite3Connector())
        investors = dao.get_investors_by_name('admin')
        self.assertIsNotNone(investors)
        self.assertFalse(len(investors) == 0)
        self.assertEqual(1, len(investors))
        self.assertTrue(isinstance(investors[0], Investor))
        names = {investor.username for investor in investors}
        self.assertFalse(len(names) == 0)
        self.assertEqual(1, len(names))
        self.assertEqual('admin', names.pop())

    def test_update_investor_status(self):
        dao = InvestorDAO(SqlLite3Connector())
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
        dao = InvestorDAO(SqlLite3Connector())
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
    
    def test_create_investor(self):
        dao = InvestorDAO(SqlLite3Connector())
        # before creating new investor
        investors = dao.get_active_investors()
        self.assertEqual(2, len(investors))
        # add new investor
        new_investor = dao.create_investor('user3')
        investors = dao.get_active_investors()
        self.assertEqual(3, len(investors))
        self.assertIsNotNone(new_investor)
        self.assertEqual('user3', new_investor.username)
        self.assertEqual('ACTIVE', new_investor.status)