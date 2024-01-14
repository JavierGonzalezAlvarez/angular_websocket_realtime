import logging
import os
from contextlib import contextmanager

import psycopg2

from utils.logging import apply_logging_conf

apply_logging_conf()

logger = logging.getLogger()

HOST = os.environ.get("HOST", "db_postgres")


def get_conexion() -> str:
    """
    use .env to keep values in production and not show them
    """
    try:
        return psycopg2.connect(host=HOST, dbname="db", user="db", password="db")
    except psycopg2.OperationalError as e:
        logger.info(f"Error: {e}")
        raise RuntimeError("Error connecting to the database")


class DbPostgresManager:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.conexion = None

    def __enter__(self):
        conn_string = f"host='{self.host}' dbname='{self.database}' user='{self.user}' password='{self.password}'"
        self.conexion = psycopg2.connect(conn_string)
        self.cursor = self.conexion.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        if self.conexion:
            self.conexion.close()


@contextmanager
def db_postgres(host, database, user, password):
    conn_string = (
        f"host='{host}' dbname='{database}' user='{user}' password='{password}'"
    )
    conexion = psycopg2.connect(conn_string)
    cursor = conexion.cursor()
    yield cursor
    cursor.close()
    conexion.close()
