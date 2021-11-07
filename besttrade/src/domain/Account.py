import json

class Account():
    def __init__(self, investor_id: int, balance: float, account_number: int = -1):
        self.account_number = account_number
        self.investor_id = investor_id
        self.balance = balance

    def __str__(self):
        return f'{{ account_number: {self.account_number}, investor_id: {self.investor_id}, balance: {self.balance} }}'

    def __eq__(self, other):
        if other is None:
            return False
        if isinstance(other, Account) == False:
            return False
        if self.investor_id == other.investor_id and self.account_number == other.account_number and self.balance == other.balance:
            return True
        return False

class AccountDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj) -> Account:
        if isinstance(obj, dict):
            d: dict[str] = obj
            if all(x in ['investor_id', 'balance', 'account_number'] for x in d.keys()):
                return Account(d.get('investor_id'), d.get('balance'), d.get('account_number'))
        return None

