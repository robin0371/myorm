import datetime

import psycopg2
import pytest

from myorm.backend.postgresql import make_connection


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
    def test_ok(self, user_model):
        user = user_model(
            name="John Doe", is_active=True, created_at=datetime.date.today()
        )

        user.objects.using(DB).save()

        assert user.id

    def test_incorrect_db(self, user_model):
        user = user_model(
            name="John Doe", is_active=True, created_at=datetime.date.today()
        )

        with pytest.raises(KeyError):
            user.objects.using("not_existed").save()


class TestRead:
    def test_get_all(self, user_model):
        user = user_model(
            name="John Doe", is_active=True, created_at=datetime.date.today()
        )

        user.objects.using(DB).save()

        users = user_model().objects.using(DB).all()

        assert len(users)
