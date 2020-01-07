"""myorm sqlite operations module."""
import copy
import logging
import os
import sqlite3

from myorm.backend.base import (
    Operations as BaseOperations,
    BaseCreateOperations,
    BaseReadOperations,
    BaseUpdateOperations,
    BaseDeleteOperations,
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
        super(Operations, self).__init__(params)

        # Operations
        self.create = CreateOperation(params)
        self.read = ReadOperation(params)
        self.update = UpdateOperation(params)
        self.delete = DeleteOperation(params)


class CreateOperation(BaseCreateOperations):
    """Create operation for MySQL database."""

    def execute(self, *, query=None, values=None):
        conn = make_connection(self.params)

        try:
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()

            obj_id = cursor.lastrowid
        except sqlite3.DatabaseError as error:
            LOGGER.error(error)
        finally:
            conn.close()

        return obj_id

    def get_query(self, *, table=None, columns=None):
        s = ("?, " * len(columns))[:-2]
        return f"{self.statement()} {table}({', '.join(columns)}) VALUES ({s});"


class ReadOperation(BaseReadOperations):
    """Read operation for SQLite database."""

    def execute(self, *, query=None):
        conn = make_connection(self.params)

        try:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
        except sqlite3.DatabaseError as error:
            LOGGER.error(error)
        finally:
            conn.close()

        return rows

    def get_query(self, *, table=None, columns=None):
        return f"{self.statement()} {', '.join(columns)} FROM {table};"


class UpdateOperation(BaseUpdateOperations):
    """Update operation for SQLite database."""

    def execute(self, *, query=None, values=None, pk=None):
        conn = make_connection(self.params)

        try:
            params = copy.copy(values)
            params.append(pk)

            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
        except sqlite3.DatabaseError as error:
            LOGGER.error(error)
        finally:
            conn.close()

    def get_query(self, *, table=None, columns=None):
        set_values = ", ".join([f"{col} = ?" for col in columns])
        return f"{self.statement()} {table} SET {set_values} WHERE id = ?;"


class DeleteOperation(BaseDeleteOperations):
    """Delete operation for SQLite database."""

    def execute(self, *, query=None, pk=None):
        conn = make_connection(self.params)

        try:
            cursor = conn.cursor()
            cursor.execute(query, (pk,))

            conn.commit()
        except sqlite3.DatabaseError as error:
            LOGGER.error(error)
        finally:
            conn.close()

    def get_query(self, *, table=None):
        return f"{self.statement()} FROM {table} WHERE id = ?;"
