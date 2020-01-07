"""myorm postgresql operations."""
import logging

import psycopg2
from psycopg2 import sql

from myorm.backend.base import (
    Operations as BaseOperations,
    BaseCreateOperations,
    BaseReadOperations,
    BaseDeleteOperations,
)

LOGGER = logging.getLogger(__name__)


def make_connection(params):
    """Return connection to PostgreSQL database."""
    connection = psycopg2.connect(**params)

    return connection


class Operations(BaseOperations):
    """Object with set of operations for PostgreSQL database."""

    def __init__(self, params):
        self.params = params

        # Operations
        self.create = CreateOperation(params)
        self.read = ReadOperation(params)
        self.delete = DeleteOperation(params)


class CreateOperation(BaseCreateOperations):
    """Create operation for PostgreSQL database."""

    def __init__(self, params):
        self.params = params

    def execute(self, *, query=None, values=None):
        conn = make_connection(self.params)

        try:
            with conn.cursor() as cursor:
                cursor.execute(sql.SQL(query), values)
                conn.commit()

                obj_id = cursor.fetchone()[0]
        except psycopg2.DatabaseError as error:
            LOGGER.error(error)
        finally:
            conn.close()

        return obj_id

    def get_query(self, *, table=None, columns=None):
        query = self.insert()
        s = ("%s, " * len(columns))[:-2]
        return f"{query} {table} ({', '.join(columns)}) VALUES ({s}) RETURNING id;"


class ReadOperation(BaseReadOperations):
    """Read operation for PostgreSQL database."""

    def __init__(self, params):
        self.params = params

    def execute(self, *, query=None):
        conn = make_connection(self.params)

        try:
            with conn.cursor() as cursor:
                cursor.execute(sql.SQL(query))

                rows = cursor.fetchall()
        except psycopg2.DatabaseError as error:
            LOGGER.error(error)
        finally:
            conn.close()

        return rows

    def get_query(self, *, table=None, columns=None):
        query = self.select()
        return f"{query} {', '.join(columns)} FROM {table};"


class DeleteOperation(BaseDeleteOperations):
    """Delete operation for PostgreSQL database."""

    def __init__(self, params):
        self.params = params

    def execute(self, *, query=None, pk=None):
        conn = make_connection(self.params)

        try:
            with conn.cursor() as cursor:
                cursor.execute(sql.SQL(query), (pk,))

            conn.commit()
        except psycopg2.DatabaseError as error:
            LOGGER.error(error)
        finally:
            conn.close()

    def get_query(self, *, table=None):
        query = self.delete()
        return f"{query} FROM {table} WHERE id = %s;"
