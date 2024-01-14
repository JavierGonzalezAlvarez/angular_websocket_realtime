import asyncio
import logging
from typing import LiteralString

import psycopg2

from utils.conexion import get_conexion
from utils.constants import INSERT_DATA_IN_TABLE
from utils.logging import apply_logging_conf

logger = logging.getLogger()

Cursor = list[str]


def run_insert(sql: LiteralString, check_table, table_name) -> Cursor:
    try:
        conexion = get_conexion()
        cursor = conexion.cursor()
        cursor.execute(check_table)
        table_exists = cursor.fetchone()[0]

        query, values = sql
        if table_exists:
            data = values

            for data in data:
                cursor.execute(query, data)
                conexion.commit()
                logger.info(f"data inserted in table: {table_name}")
            return
        else:
            logger.info(f"table {table_name} doesn't exists yet")

        cursor.close()
        conexion.close()

    except (Exception, psycopg2.Error) as error:
        return f"conexion error: {error}"


def caller_insert(
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

    run_insert(query_string, check_table, table_name)


async def main():
    caller_insert(INSERT_DATA_IN_TABLE.status, "status")
    caller_insert(INSERT_DATA_IN_TABLE.machines, "machines")
    caller_insert(INSERT_DATA_IN_TABLE.model, "model")


if __name__ == "__main__":
    apply_logging_conf()
    asyncio.run(main())
