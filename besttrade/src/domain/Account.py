class Account():
    def __init__(self, investor_id: int, balance: float, account_number: int = -1):
        self.account_number = account_number
        self.investor_id = investor_id
        self.balance = balance

    def __str__(self):
        return f'{{ account_number: {self.account_number}, investor_id: {self.investor_id}, balance: {self.balance} }}'
