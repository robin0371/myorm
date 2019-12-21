"""myorm sqlite operations module."""
import os
import sqlite3


def make_connection(params):
    """Return connection to SQLite database."""
    db = params.get("db")

    if not db:
        raise ConnectionError("params haven't 'db' key or 'db' is empty")

    if not os.path.exists(db):
        raise ConnectionError("db file does not exist")

    connection = sqlite3.connect(db)

    return connection
