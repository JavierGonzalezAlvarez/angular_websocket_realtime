import asyncio
import logging

import psycopg2

from utils.conexion import get_conexion
from utils.logging import apply_logging_conf

apply_logging_conf()
logger = logging.getLogger()

total_duration_seconds = 5 * 60  # X minutes * X seconds
interval_seconds = 10  # X-second interval

data_queue = asyncio.Queue()


def insert_data_simulation(sql, values, check_table, table_name) -> []:
    try:
        conexion = get_conexion()
        cursor = conexion.cursor()
        cursor.execute(check_table)
        table_exists = cursor.fetchone()[0]

        if table_exists:
            for data in values:
                cursor.execute(sql, data)
                conexion.commit()
                logger.info(f"record {values} saved in table: {table_name}")
            return values
        else:
            logger.info(f"table {table_name} doesn't exists yet")

        cursor.close()
        conexion.close()
        return []

    except (Exception, psycopg2.Error) as error:
        return f"conexion error: {error}"


def set_data_to_send(data: list = []):
    # setter for WEBSOCKET
    logger.info(f"data {data}")
    data_queue.put_nowait(data)


def get_data_to_send():
    # getter for WEBSOCKET
    return data_queue.get()


def insert_data_model(sql, data, check_table, table_name):
    """
    Insert data in data_model table when model is running in real time.

    :param sql: the sql sentence to be run
    :param data: bla, bla, ...
    :param check_table: bla, bla, ...
    :param table_name: bla, bla, ...
    """
    try:
        conexion = get_conexion()
        cursor = conexion.cursor()
        cursor.execute(check_table)
        table_exists = cursor.fetchone()[0]

        if table_exists:
            cursor.execute(sql, data[0])
            conexion.commit()
            logger.info(f"{data[0]} saved, table: {table_name}")
            set_data_to_send(data[0])
        else:
            logger.info(f"table {table_name} doesn't exists yet")

        cursor.close()
        conexion.close()

    except (Exception, psycopg2.Error) as error:
        return f"conexion error: {error}"


def check_table_exists(table_name: str, cursor) -> bool:
    cursor.execute(
        f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}')"
    )
    return cursor.fetchone()[0]
