import typing as t
from contextlib import closing
from besttrade.src.domain import Account
from .AbstractDatabaseConnector import AbstractDatabaseConnector
from besttrade.src.db import sqlscripts as sql, DaoException

class AccountDAO():
    def __init__(self, connector: AbstractDatabaseConnector):
        assert(isinstance(connector, AbstractDatabaseConnector))
        self.connector = connector

    def get_cnx(self):
        return self.connector.get_connection()

    def get_all_accounts(self) -> t.List[Account]:
        try:
            with self.get_connection() as cnx:
                with closing(cnx.cursor()) as cur:
                    query = sql.get_accounts
                    cur.execute(query)
                    rows = cur.fetchall()
                    if len(rows) == 0:
                        return []
                    accounts = []
                    for row in rows:
                        accounts.append(
                            Account(investor_id=row[0], balance=row[1], account_number=row[2]))
                    return accounts
        except Exception as e:
            raise DaoException(
                f'Unable to get list of all accounts: {str(e)}')

    def get_account_by_id(self, account_number: int) -> t.Optional[Account]:
        try:
            with self.connector.get_connection() as cnx:
                with closing(cnx.cursor()) as cur:
                    query = sql.get_account_by_id
                    cur.execute(query, (account_number, ))
                    rows = cur.fetchall()
                    if len(rows) == 0:
                        return None
                    if len(rows) > 1:
                        raise DaoException(
                            f'Unexpected result: found {cur.rowcount} records for account with ID {account_number}.')
                    row = rows[0]  # only one account for a given ID
                    investor_id, balance, account_number = row
                    return Account(investor_id, balance, account_number)
        except Exception as e:
            raise DaoException(
                f'Failed to return account with ID {account_number}: {str(e)}')

    def get_account_by_investor_id(self, investor_id: int) -> t.List[Account]:
        try:
            with self.connector.get_connection() as cnx:
                with closing(cnx.cursor()) as cur:
                    q = sql.get_accounts_by_investor_id
                    cur.execute(q, (investor_id, ))
                    rows = cur.fetchall()
                    if len(rows) == 0:
                        return []
                    accounts = []
                    for row in rows:
                        investorId, balance, account_number = row
                        accounts.append(
                            Account(investorId, balance, account_number))
                    return accounts
        except Exception as e:
            raise DaoException(
                f'Failed to get accounts for investor with ID {investor_id}: {str(e)}')

    def delete_account(self, account_number: int) -> None:
        try:
            with self.connector.get_connection() as cnx:
                with closing(cnx.cursor()) as cur:
                    q = sql.delete_account
                    cur.execute(q, (account_number, ))
                    cnx.commit()
        except Exception as e:
            raise DaoException(
                f'Failed to delete account with ID {account_number}: {str(e)}')

    def update_account_balance(self, account_number: int, balance: float) -> None:
        try:
            with self.connector.get_connection() as cnx:
                with closing(cnx.cursor()) as cur:
                    q = sql.update_account_balance
                    cur.execute(q, (balance, account_number))
                    cnx.commit()
        except Exception as e:
            raise DaoException(
                f'Failed to update account {account_number} balance to {balance}: {str(e)}')

    def create_account(self, investor_id: int, balance: int) -> Account:
        try:
            with self.connector.get_connection() as cnx:
                with closing(cnx.cursor()) as cur:
                    q = sql.create_account
                    cur.execute(q, (investor_id, balance))
                    account_number = cur.lastrowid
                    return Account(investor_id=investor_id, balance=balance, account_number=account_number)
        except Exception as e:
            raise DaoException(
                f'Failed to create a new account for investor {investor_id}: {str(e)}')
