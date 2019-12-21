import pymysql
import pytest

from myorm.backend.mysql import make_connection


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
