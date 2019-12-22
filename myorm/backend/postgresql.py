"""myorm postgresql operations."""
import logging

import psycopg2
from psycopg2 import sql

from myorm.backend.base import (
    Operations as BaseOperations,
    BaseCreateOperations,
    BaseReadOperations,
)

LOGGER = logging.getLogger(__name__)


def make_connection(params):
    """Return connection to PostgreSQL database."""
    connection = psycopg2.connect(**params)

    return connection


class Operations(BaseOperations):
    """Object with set of operations for PostgreSQL database."""

    def __init__(self, params):
        self.connection = make_connection(params)

        # Operations
        self.create = CreateOperation(self.connection)
        self.read = ReadOperation(self.connection)


class CreateOperation(BaseCreateOperations):
    """Create operation for PostgreSQL database."""

    def __init__(self, conn):
        self.connection = conn

    def execute(self, *, query=None, values=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql.SQL(query), values)

            self.connection.commit()
            obj_id = cursor.fetchone()[0]

        except psycopg2.DatabaseError as error:
            LOGGER.error(error)
        else:
            cursor.close()
            return obj_id

    def get_query(self, *, table=None, columns=None):
        query = self.insert()
        s = ("%s, " * len(columns))[:-2]
        return f"{query} {table} ({', '.join(columns)}) VALUES ({s}) RETURNING id"


class ReadOperation(BaseReadOperations):
    """Read operation for PostgreSQL database."""

    def __init__(self, conn):
        self.connection = conn

    def execute(self, *, query=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql.SQL(query))

            rows = cursor.fetchall()

        except psycopg2.DatabaseError as error:
            LOGGER.error(error)
        else:
            cursor.close()
            return rows

    def get_query(self, *, table=None, columns=None):
        query = self.select()
        return f"{query} {', '.join(columns)} FROM {table}"
