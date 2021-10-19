import typing as t
from .AbstractDatabaseConnector import AbstractDatabaseConnector
from contextlib import closing
from besttrade.src.domain import Investor, Account
from .DaoException import DaoException
from besttrade.src.db import sqlscripts as sql


class DataAccessObject():
    def __init__(self, connector: AbstractDatabaseConnector):
        assert(isinstance(connector, AbstractDatabaseConnector))
        self.connector = connector

    def get_connection(self):
        return self.connector.get_connection()

    def get_investors(self) -> list[Investor]:
        '''
            Returns a list of all investors (both active and inactive)
        '''
        try:
            with self.get_connection() as cnx:
                with closing(cnx.cursor()) as cursor:
                    cursor.execute(sql.all_investors_sql)
                    investors = []
                    rows = cursor.fetchall()
                    for row in rows:
                        name, status, id = row
                        investors.append(Investor(name, status, id))
                    return investors
        except Exception as e:
            raise DaoException(
                f'Failed to retrieve list of investors: {str(e)}')

    def get_active_investors(self) -> list[Investor]:
        '''
            Returns a list of all active investors
        '''
        try:
            with self.get_connection() as cnx:
                with closing(cnx.cursor()) as cursor:
                    cursor.execute(sql.all_active_investors_sql)
                    investors = []
                    rows = cursor.fetchall()
                    for row in rows:
                        name, status, id = row
                        investors.append(Investor(name, status, id))
                    return investors
        except Exception as e:
            raise DaoException(
                f'Failed to retrieve list of investors: {str(e)}')

    def get_investor_by_id(self, id: int) -> t.Optional[Investor]:
        '''
            Get investor by id
        '''
        try:
            with self.connector.get_connection() as cnx:
                with closing(cnx.cursor()) as cur:
                    query = sql.investor_by_id_sql
                    cur.execute(query, (id,))
                    if (cur.rowcount > 1):
                        raise DaoException(
                            f'Unexpected result: found more than one investor with id {id}')
                    if (cur.rowcount == 0):
                        return None
                    row = cur.fetchone()
                    return Investor(row[0], row[1], row[2])
        except Exception as e:
            raise DaoException(
                f'Failed to retrieve investor with id {id}: {str(e)}')

    def get_investors_by_name(self, name: str) -> list[Investor]:
        try:
            with self.connector.get_connection() as cnx:
                with closing(cnx.cursor()) as cur:
                    query = sql.get_investors_by_name
                    cur.execute(query, (name, ))
                    if cur.rowcount == 0:
                        return []
                    investors = []
                    for row in cur.fetchall():
                        investors.append(
                            Investor(username=row[0], status=row[1], id=row[2]))
                    return investors
        except Exception as e:
            raise DaoException(
                f'Failed to get list of investors with {name} name: {str(e)}')

    def create_investor(self, username) -> Investor:
        '''
            Creates a new investor. All new investors are initially set to ACTIVE.
        '''
        try:
            with self.get_connection() as cnx:
                with closing(cnx.cursor()) as cursor:
                    query = sql.new_investor_sql
                    cursor.execute(query, (username,))
                    cnx.commit()
                    return Investor(username, 'ACTIVE', cursor.lastrowid)
        except Exception as e:
            raise DaoException(f'Failed to create new investor: {str(e)}')

    def update_investor_name(self, id: int, name: str) -> None:
        try:
            with self.connector.get_connection() as cnx:
                with closing(cnx.cursor()) as cur:
                    query = sql.update_investor_by_name
                    cur.execute(query, (name, id))
                    cnx.commit()
        except Exception as e:
            raise DaoException(
                f'Unable to update investor {id} name to {name}: {str(e)}')

    def update_investor_status(self, id: int, status: str) -> None:
        try:
            with self.get_connection() as cnx:
                with closing(cnx.cursor()) as cur:
                    query = sql.update_investor_status
                    cur.execute(query, (status, id))
                    cnx.commit()
        except Exception as e:
            raise DaoException(
                f'Unable to update investor {id} to {status} status: {str(e)}')

    def get_all_accounts(self) -> list[Account]:
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

    def get_account_by_investor_id(self, investor_id: int) -> list[Account]:
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
