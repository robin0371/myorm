import os

import pytest


def get_project_root():
    return os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]


@pytest.fixture(scope='session')
def postgres_db_params():
    test_db_params = {
        "host": "localhost",
        "port": 54320,
        "user": "myorm_user",
        "password": "myorm_user",
        "database": "myorm_db",
    }
    return test_db_params


@pytest.fixture(scope='session')
def mysql_db_params():
    test_db_params = {
        "host": "localhost",
        "user": "myorm_user",
        "password": "myorm_user",
        "database": "myorm_db",
    }
    return test_db_params


@pytest.fixture(scope='session')
def sqlite_db_params():
    test_db_params = {
        "db": os.path.join(get_project_root(), "db", "sqlite.db"),
    }
    return test_db_params
