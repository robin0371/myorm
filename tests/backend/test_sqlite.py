import datetime
import sqlite3

import pytest

from myorm.backend.sqlite import make_connection
from tests.conftest import User

DB = "sqlite"


class TestMakeConnection:
    @pytest.mark.parametrize(
        "params,expectation",
        [
            ({}, pytest.raises(ConnectionError)),
            ({"db": "notexisted.db"}, pytest.raises(ConnectionError)),
        ],
    )
    def test_params(self, params, expectation):
        with expectation:
            make_connection(params)

    def test_ok(self, sqlite_db_params):
        connection = make_connection(sqlite_db_params)
        assert isinstance(connection, sqlite3.Connection)
        connection.close()


class TestCreate:
    def test_ok(self, sqlite_session):
        user = User(name="John Doe", is_active=True, created_at=datetime.date.today())

        user.objects.using(DB).save()

        assert user.pk == 1
        assert user.name == "John Doe"
        assert user.is_active is True
        assert user.created_at == datetime.date.today()

    def test_no_active(self, sqlite_session):
        user = User(name="John Doe", is_active=False, created_at=datetime.date.today())

        user.objects.using(DB).save()

        assert user.pk == 1
        assert user.name == "John Doe"
        assert user.is_active is False
        assert user.created_at == datetime.date.today()

    def test_incorrect_db(self, sqlite_session):
        user = User(name="John Doe", is_active=True, created_at=datetime.date.today())

        with pytest.raises(KeyError):
            user.objects.using("not_existed").save()


class TestRead:
    def test_get_all(self, sqlite_session):
        user = User(name="J Doe", is_active=True, created_at=datetime.date.today())
        user.objects.using(DB).save()
        assert user.pk == 1

        users = User().objects.using(DB).all()

        assert len(users) == 1

        first_user = users[0]

        assert first_user.pk == 1
        assert first_user.name == "J Doe"
        assert first_user.is_active is True
        assert first_user.created_at == datetime.date.today()

    def test_get_first(self, sqlite_session):
        user = User(name="M Doe", is_active=True, created_at=datetime.date.today())
        user.objects.using(DB).save()
        assert user.pk == 1

        first_user = User().objects.using(DB).first()

        assert first_user.pk == 1
        assert first_user.name == "M Doe"
        assert first_user.is_active is True
        assert first_user.created_at == datetime.date.today()

    def test_get_last(self, sqlite_session):
        user = User(name="B Doe", is_active=True, created_at=datetime.date.today())
        user.objects.using(DB).save()
        assert user.pk == 1

        first_user = User().objects.using(DB).last()

        assert first_user.pk == 1
        assert first_user.name == "B Doe"
        assert first_user.is_active is True
        assert first_user.created_at == datetime.date.today()


class TestDelete:
    def test_ok(self, sqlite_session):
        user = User(name="G Doe", is_active=True, created_at=datetime.date.today())
        user.objects.using(DB).save()

        assert user.pk == 1

        users = User().objects.using(DB).all()
        assert len(users) == 1

        user.delete()
        assert user.pk is None

        users = User().objects.using(DB).all()
        assert len(users) == 0
