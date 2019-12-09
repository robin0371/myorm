import pymysql


def make_connection(params):
    connection = pymysql.connect(**params)

    return connection
