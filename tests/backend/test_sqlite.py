import sqlite3

import pytest

from myorm.backend.sqlite import make_connection


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
