import psycopg2


def make_connection(params):
    connection = psycopg2.connect(**params)

    return connection
