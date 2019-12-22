"""myorm sqlite operations module."""
import logging
import os
import sqlite3

from myorm.backend.base import (
    Operations as BaseOperations,
    BaseCreateOperations,
    BaseReadOperations,
)


LOGGER = logging.getLogger(__name__)


def make_connection(params):
    """Return connection to SQLite database."""
    db = params.get("db")

    if not db:
        raise ConnectionError("params haven't 'db' key or 'db' is empty")

    if not os.path.exists(db):
        raise ConnectionError("db file does not exist")

    connection = sqlite3.connect(db)

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
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute(query, values)

                obj_id = cursor.lastrowid
        except sqlite3.DatabaseError as error:
            LOGGER.error(error)
        else:
            return obj_id

    def get_query(self, *, table=None, columns=None):
        query = self.insert()
        s = ("?, " * len(columns))[:-2]
        return f"{query} {table}({', '.join(columns)}) VALUES ({s})"


class ReadOperation(BaseReadOperations):
    """Read operation for SQLite database."""

    def __init__(self, conn):
        self.connection = conn

    def execute(self, *, query=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)

            rows = cursor.fetchall()
        except sqlite3.DatabaseError as error:
            LOGGER.error(error)
        else:
            return rows

    def get_query(self, *, table=None, columns=None):
        query = self.select()
        return f"{query} {', '.join(columns)} FROM {table}"
