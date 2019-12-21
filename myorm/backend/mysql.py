"""myorm mysql operations module."""
import pymysql


def make_connection(params):
    """Return connection to MySQL database."""
    connection = pymysql.connect(**params)

    return connection
