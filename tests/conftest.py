import pytest
from psycopg2 import sql

from myorm import Model, BooleanField, CharField, DateField, IntegerField
from myorm.backend.postgresql import make_connection as postgres_make_connection
from myorm.backend.mysql import make_connection as mysql_make_connection
from myorm.backend.sqlite import make_connection as sqlite_make_connection
from myorm.db import DATABASES


class User(Model):
    id = IntegerField()
    name = CharField()
    is_active = BooleanField()
    created_at = DateField()


@pytest.fixture(scope="function")
def postgres_clean(postgres_db_params):
    """Clean users table in PostgreSQL database."""
    with postgres_make_connection(postgres_db_params) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql.SQL("TRUNCATE users RESTART IDENTITY;"))
            connection.commit()
            cursor.close()

            if connection.closed != 0:
                connection.close()
    yield


@pytest.fixture(scope="function")
def mysql_clean(mysql_db_params):
    """Clean users table in MySQL database."""
    connection = mysql_make_connection(mysql_db_params)
    with connection.cursor() as cursor:
        cursor.execute("TRUNCATE users;")
        connection.commit()
        cursor.close()
    connection.close()
    yield


@pytest.fixture(scope="function")
def sqlite_clean(sqlite_db_params):
    """Clean users table in SQLite database."""
    connection = sqlite_make_connection(sqlite_db_params)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users;")
    connection.commit()
    cursor.close()
    connection.close()
    yield


@pytest.fixture(scope="session")
def postgres_db_params():
    return DATABASES["postgres"]


@pytest.fixture(scope="session")
def mysql_db_params():
    return DATABASES["mysql"]


@pytest.fixture(scope="session")
def sqlite_db_params():
    return DATABASES["sqlite"]
