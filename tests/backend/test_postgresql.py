import psycopg2
import pytest

from myorm.backend.postgresql import make_connection


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
