"""myorm postgresql operations."""
import copy
import logging

import psycopg2
from psycopg2 import sql

from myorm.backend.base import (
    Operations as BaseOperations,
    BaseCreateOperations,
    BaseReadOperations,
    BaseUpdateOperations,
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
        super(Operations, self).__init__(params)

        # Operations
        self.create = CreateOperation(params)
        self.read = ReadOperation(params)
        self.update = UpdateOperation(params)
        self.delete = DeleteOperation(params)


class CreateOperation(BaseCreateOperations):
    """Create operation for PostgreSQL database."""

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
        s = ("%s, " * len(columns))[:-2]
        return f"{self.statement()} {table} ({', '.join(columns)}) VALUES ({s}) RETURNING id;"


class ReadOperation(BaseReadOperations):
    """Read operation for PostgreSQL database."""

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
        return f"{self.statement()} {', '.join(columns)} FROM {table};"


class UpdateOperation(BaseUpdateOperations):
    """Update operation for PostgreSQL database."""

    def execute(self, *, query=None, values=None, pk=None):
        conn = make_connection(self.params)

        try:
            params = copy.copy(values)
            params.append(pk)

            with conn.cursor() as cursor:
                cursor.execute(sql.SQL(query), params)
                conn.commit()

        except psycopg2.DatabaseError as error:
            LOGGER.error(error)
        finally:
            conn.close()

    def get_query(self, *, table=None, columns=None):
        set_values = ", ".join([f"{col} = %s" for col in columns])
        return f"{self.statement()} {table} SET {set_values} WHERE id = %s;"


class DeleteOperation(BaseDeleteOperations):
    """Delete operation for PostgreSQL database."""

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
        return f"{self.statement()} FROM {table} WHERE id = %s;"
