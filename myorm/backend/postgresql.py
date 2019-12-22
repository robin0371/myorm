"""myorm postgresql operations."""
import logging

import psycopg2
from psycopg2 import sql

from myorm.backend.base import (
    Operations as BaseOperations,
    BaseCreateOperations,
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
        self.create = CreateOperation(self.connection)

    def make_connection(self):
        self.connection = make_connection(self.params)


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
