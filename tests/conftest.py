import os

import pytest


from myorm import Model, BooleanField, CharField, DateTimeField, IntegerField
from myorm.util import get_project_root


class User(Model):
    id = IntegerField()
    name = CharField()
    is_active = BooleanField()
    created_at = DateTimeField()


@pytest.fixture(scope="session")
def user_model():
    return User


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
