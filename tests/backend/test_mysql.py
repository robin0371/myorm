import datetime

import pymysql
import pytest

from myorm.backend.mysql import make_connection


DB = "mysql"


class TestMakeConnection:
    @pytest.mark.parametrize(
        "params,expectation",
        [
            ({}, pytest.raises(pymysql.err.OperationalError)),
            ({"database": "notexisted"}, pytest.raises(pymysql.err.OperationalError)),
        ],
    )
    def test_params(self, params, expectation):
        with expectation:
            make_connection(params)

    def test_ok(self, mysql_db_params):
        connection = make_connection(mysql_db_params)
        assert connection.open
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
