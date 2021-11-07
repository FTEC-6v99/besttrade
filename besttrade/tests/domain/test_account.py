import unittest
import json
from besttrade.src.domain import Account, AccountDecoder

class TestAccount(unittest.TestCase):
    def test_eq(self):
        a1 = Account(101, 100.00, 1)
        a2 = Account(101, 100.00, 1)
        self.assertTrue(a1.__eq__(a2))
        a3 = Account(101, 100.0, 2)
        self.assertFalse(a2.__eq__(a3))
        self.assertFalse(a2.__eq__('String datatype'))

    def test_account_serialize(self):
        a1 = Account(101, 1000.00, 1)
        a1_json = json.dumps(a1, default= lambda x: x.__dict__, sort_keys=True)
        expected = '{"account_number": 1, "balance": 1000.0, "investor_id": 101}'
        self.assertIsNotNone(a1_json)
        self.assertEqual(expected, a1_json)

    def test_account_deserialize(self):
        input = '{"account_number": 1, "balance": 1000.0, "investor_id": 101}'
        actual = json.loads(input, cls=AccountDecoder)
        self.assertIsNotNone(actual)
        self.assertTrue(isinstance(actual, Account))
        expected = Account(101, 1000.0, 1)
        self.assertTrue(expected, actual)