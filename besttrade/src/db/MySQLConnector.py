from mysql.connector import connect
from .AbstractDatabaseConnector import AbstractDatabaseConnector


class MySQLConnector(AbstractDatabaseConnector):
    def __init__(self, config: dict = {}):
        required = ['user', 'password', 'host', 'db']
        if all(key in config.keys() for key in required) == False:
            raise ConnectionError(
                'One of required arguments for MySQL connection is missing')
        self.config = config
        super().__init__()

    def get_connection(self):
        return connect(**self.config)
