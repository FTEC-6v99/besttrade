import typing as t
from .AbstractDatabaseConnector import AbstractDatabaseConnector
from contextlib import closing
from besttrade.src.domain import Investor
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
