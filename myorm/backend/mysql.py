"""myorm mysql operations module."""
import logging

import pymysql

from myorm.backend.base import (
    Operations as BaseOperations,
    BaseCreateOperations,
)

LOGGER = logging.getLogger(__name__)


def make_connection(params):
    """Return connection to MySQL database."""
    connection = pymysql.connect(**params)

    return connection


class Operations(BaseOperations):
    """Object with set of operations for MySQL database."""

    def __init__(self, params):
        super(Operations, self).__init__(params)
        self.create = CreateOperation(self.connection)

    def make_connection(self):
        self.connection = make_connection(self.params)


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
