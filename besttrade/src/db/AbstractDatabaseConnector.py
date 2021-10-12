import typing as t
from abc import ABC, abstractmethod
from mysql.connector import MySQLConnection
from sqlite3 import Connection


class AbstractDatabaseConnector(ABC):

    @abstractmethod
    def get_connection(self) -> t.Union[MySQLConnection, Connection]:
        ...
