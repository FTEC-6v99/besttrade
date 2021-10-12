from sqlite3 import connect
from besttrade.src.db import AbstractDatabaseConnector


class SqlLite3Connector(AbstractDatabaseConnector):
    def __init__(self):
        super().__init__()

    def get_connection(self):
        return connect('testdb.db')
