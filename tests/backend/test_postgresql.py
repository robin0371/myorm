import datetime

import psycopg2
import pytest

from myorm.backend.postgresql import make_connection
from tests.conftest import User

DB = "postgres"


class TestMakeConnection:
    @pytest.mark.parametrize(
        "params,expectation",
        [
            ({}, pytest.raises(TypeError)),
            ({"database": "notexisted"}, pytest.raises(psycopg2.OperationalError)),
        ],
    )
    def test_params(self, params, expectation):
        with expectation:
            make_connection(params)

    def test_ok(self, postgres_db_params):
        connection = make_connection(postgres_db_params)
        assert connection.status == psycopg2.extensions.STATUS_READY
        connection.close()


class TestCreate:
    def test_ok(self, postgres_session):
        user = User(name="John Doe", is_active=True, created_at=datetime.date.today())

        user.objects.using(DB).save()

        assert user.pk == 1
        assert user.name == "John Doe"
        assert user.is_active is True
        assert user.created_at == datetime.date.today()

    def test_no_active(self, postgres_session):
        user = User(name="John Doe", is_active=False, created_at=datetime.date.today())

        user.objects.using(DB).save()

        assert user.pk == 1
        assert user.name == "John Doe"
        assert user.is_active is False
        assert user.created_at == datetime.date.today()

    def test_incorrect_db(self, postgres_session):
        user = User(name="John Doe", is_active=True, created_at=datetime.date.today())

        with pytest.raises(KeyError):
            user.objects.using("not_existed").save()


class TestRead:
    def test_get_all(self, postgres_session):
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

    def test_get_first(self, postgres_session):
        user = User(name="M Doe", is_active=True, created_at=datetime.date.today())
        user.objects.using(DB).save()
        assert user.pk == 1

        first_user = User().objects.using(DB).first()

        assert first_user.pk == 1
        assert first_user.name == "M Doe"
        assert first_user.is_active is True
        assert first_user.created_at == datetime.date.today()

    def test_get_last(self, postgres_session):
        user = User(name="B Doe", is_active=True, created_at=datetime.date.today())
        user.objects.using(DB).save()
        assert user.pk == 1

        first_user = User().objects.using(DB).last()

        assert first_user.pk == 1
        assert first_user.name == "B Doe"
        assert first_user.is_active is True
        assert first_user.created_at == datetime.date.today()


class TestDelete:
    def test_ok(self, postgres_session):
        user = User(name="G Doe", is_active=True, created_at=datetime.date.today())
        user.objects.using(DB).save()

        assert user.pk == 1

        users = User().objects.using(DB).all()
        assert len(users) == 1

        user.delete()
        assert user.pk is None

        users = User().objects.using(DB).all()
        assert len(users) == 0


class TestUpdate:
    def test_ok(self, postgres_session):
        user = User(name="G Doe", is_active=True, created_at=datetime.date.today())
        user.objects.using(DB).save()

        assert user.pk == 1
        assert user.name == "G Doe"
        assert user.is_active is True
        assert user.created_at == datetime.date.today()

        # update user
        user.name = "John D"
        user.is_active = False
        user.save()

        # check object
        assert user.pk == 1
        assert user.name == "John D"
        assert user.is_active is False
        assert user.created_at == datetime.date.today()

        # check database
        first_user = User().objects.using(DB).first()

        assert first_user.pk == 1
        assert first_user.name == "John D"
        assert first_user.is_active is False
        assert first_user.created_at == datetime.date.today()
