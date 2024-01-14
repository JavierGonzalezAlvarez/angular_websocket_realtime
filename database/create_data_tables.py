# this code creates tables if doesn't exist

import asyncio
import logging
from typing import LiteralString

import psycopg2

from utils.conexion import get_conexion
from utils.constants import CREATE_TABLE
from utils.logging import apply_logging_conf

logger = logging.getLogger()

Cursor = list[str]


def run_create(sql: LiteralString, check_table, table_name) -> Cursor:
    try:
        conexion = get_conexion()
        cursor = conexion.cursor()

        cursor.execute(check_table)
        table_exists = cursor.fetchone()[0]

        if table_exists:
            logger.info(f"table {table_name} already exists")
            return
        else:
            cursor.execute(sql)
            conexion.commit()
            logger.info(f"table {table_name} created")
        cursor.close()
        conexion.close()

    except (Exception, psycopg2.Error) as error:
        return f"conexion error: {error}"


def caller(
    query_string: LiteralString,
    table_name: LiteralString | None,
) -> bool:
    """
    PEP 675: Arbitrary literal string type
    """

    check_table = f"""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = '{table_name}'
        );
    """

    run_create(query_string, check_table, table_name)


async def main():
    caller(CREATE_TABLE.model, "model")  # (sql, name of the table)
    caller(CREATE_TABLE.simulation, "simulation")
    caller(CREATE_TABLE.status, "status")
    caller(CREATE_TABLE.machines, "machines")
    caller(CREATE_TABLE.data_model, "data_model")


if __name__ == "__main__":
    apply_logging_conf()
    asyncio.run(main())
