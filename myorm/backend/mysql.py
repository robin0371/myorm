"""myorm mysql operations module."""
import logging

import pymysql

from myorm.backend.base import (
    Operations as BaseOperations,
    BaseCreateOperations,
    BaseReadOperations,
    BaseDeleteOperations,
)

LOGGER = logging.getLogger(__name__)


def make_connection(params):
    """Return connection to MySQL database."""
    connection = pymysql.connect(**params)

    return connection


class Operations(BaseOperations):
    """Object with set of operations for MySQL database."""

    def __init__(self, params):
        self.params = params

        # Operations
        self.create = CreateOperation(params)
        self.read = ReadOperation(params)
        self.delete = DeleteOperation(params)


class CreateOperation(BaseCreateOperations):
    """Create operation for MySQL database."""

    def __init__(self, params):
        self.params = params

    def execute(self, *, query=None, values=None):
        conn = make_connection(self.params)

        try:
            with conn.cursor() as cursor:
                cursor.execute(query, values)
                obj_id = cursor.lastrowid

            conn.commit()
        except pymysql.DatabaseError as error:
            LOGGER.error(error)
        finally:
            conn.close()

        return obj_id

    def get_query(self, *, table=None, columns=None):
        s = ("%s, " * len(columns))[:-2]
        return f"{self.statement()} {table} ({', '.join(columns)}) VALUES ({s})"


class ReadOperation(BaseReadOperations):
    """Read operation for MySQL database."""

    def __init__(self, params):
        self.params = params

    def execute(self, *, query=None):
        conn = make_connection(self.params)

        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
        except pymysql.DatabaseError as error:
            LOGGER.error(error)
        finally:
            conn.close()

        return rows

    def get_query(self, *, table=None, columns=None):
        return f"{self.statement()} {', '.join(columns)} FROM {table}"


class DeleteOperation(BaseDeleteOperations):
    """Delete operation for MySQL database."""

    def __init__(self, params):
        self.params = params

    def execute(self, *, query=None, pk=None):
        conn = make_connection(self.params)

        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (pk,))

            conn.commit()
        except pymysql.DatabaseError as error:
            LOGGER.error(error)
        finally:
            conn.close()

    def get_query(self, *, table=None):
        return f"{self.statement()} FROM {table} WHERE id = %s;"
