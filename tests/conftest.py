import os

import pytest
from psycopg2 import sql

from myorm import Model, BooleanField, CharField, DateTimeField, IntegerField
from myorm.backend.postgresql import make_connection as postgres_make_connection
from myorm.backend.mysql import make_connection as mysql_make_connection
from myorm.util import get_project_root


class User(Model):
    id = IntegerField()
    name = CharField()
    is_active = BooleanField()
    created_at = DateTimeField()


@pytest.fixture(scope="function")
def postgres_session(postgres_db_params):
    with postgres_make_connection(postgres_db_params) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql.SQL("TRUNCATE users RESTART IDENTITY;"))
            connection.commit()
            cursor.close()

            if connection.closed != 0:
                connection.close()
    yield


@pytest.fixture(scope="function")
def mysql_session(mysql_db_params):
    connection = mysql_make_connection(mysql_db_params)
    with connection.cursor() as cursor:
        cursor.execute("TRUNCATE users;")
        connection.commit()
        cursor.close()
    connection.close()
    yield


@pytest.fixture(scope="session")
def postgres_db_params():
    test_db_params = {
        "host": "localhost",
        "port": 54320,
        "user": "myorm_user",
        "password": "myorm_user",
        "database": "myorm_db",
    }
    return test_db_params


@pytest.fixture(scope="session")
def mysql_db_params():
    test_db_params = {
        "host": "localhost",
        "user": "myorm_user",
        "password": "myorm_user",
        "database": "myorm_db",
    }
    return test_db_params


@pytest.fixture(scope="session")
def sqlite_db_params():
    test_db_params = {
        "db": os.path.join(get_project_root(), "db", "sqlite.db"),
    }
    return test_db_params
