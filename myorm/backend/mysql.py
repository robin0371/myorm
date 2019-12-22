"""myorm mysql operations module."""
import logging

import pymysql

from myorm.backend.base import (
    Operations as BaseOperations,
    BaseCreateOperations,
    BaseReadOperations,
)

LOGGER = logging.getLogger(__name__)


def make_connection(params):
    """Return connection to MySQL database."""
    connection = pymysql.connect(**params)

    return connection


class Operations(BaseOperations):
    """Object with set of operations for MySQL database."""

    def __init__(self, params):
        self.connection = make_connection(params)

        # Operations
        self.create = CreateOperation(self.connection)
        self.read = ReadOperation(self.connection)


class CreateOperation(BaseCreateOperations):
    """Create operation for MySQL database."""

    def __init__(self, conn):
        self.connection = conn

    def execute(self, *, query=None, values=None):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, values)
                obj_id = cursor.lastrowid

            self.connection.commit()
        except pymysql.DatabaseError as error:
            LOGGER.error(error)
        else:
            return obj_id

    def get_query(self, *, table=None, columns=None):
        query = self.insert()
        s = ("%s, " * len(columns))[:-2]
        return f"{query} {table} ({', '.join(columns)}) VALUES ({s})"


class ReadOperation(BaseReadOperations):
    """Read operation for MySQL database."""

    def __init__(self, conn):
        self.connection = conn

    def execute(self, *, query=None):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
        except pymysql.DatabaseError as error:
            LOGGER.error(error)
        else:
            return rows

    def get_query(self, *, table=None, columns=None):
        query = self.select()
        return f"{query} {', '.join(columns)} FROM {table}"
