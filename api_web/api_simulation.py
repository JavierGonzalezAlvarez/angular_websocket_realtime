import asyncio
import logging
import random
import time
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Request, status

from model.model import check_table_exists, insert_data_model, insert_data_simulation
from utils.conexion import get_conexion
from utils.constants import INSERT_DATA_IN_TABLE, TABLE_NAME
from utils.logging import apply_logging_conf

apply_logging_conf()
logger = logging.getLogger()


router = APIRouter(
    prefix="/v1.0",
    tags=["simulation"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/list_simulations",
    status_code=status.HTTP_200_OK,
    responses={
        409: {"description": "..."},
        201: {"description": "List created sucessfully"},
    },
    name="list_simulation",
    summary="list a table",
    description="This endpoint lists simulations from table simulation",
)
def list_simulations() -> []:
    try:
        conexion = get_conexion()
        cursor = conexion.cursor()

        # check if exists
        if not check_table_exists(TABLE_NAME.simulation, cursor):
            cursor.close()
            conexion.close()
            return {
                "status_code": status.HTTP_409_CONFLICT,
                "message": f"Table {TABLE_NAME.simulation} does not exist",
                "data": [],
            }

        query = """SELECT simulation.*
            FROM simulation
            JOIN status ON simulation.id_status = status.id_status;
        """

        cursor.execute(
            f"SELECT column_name FROM information_schema.columns WHERE table_name = '{TABLE_NAME.simulation}';"
        )
        columns = [column[0] for column in cursor.fetchall()]

        cursor.execute(query)
        data = cursor.fetchall()

        data_list = []
        for row in data:
            result = {}
            for idx, value in enumerate(row):
                result[columns[idx]] = value
            data_list.append(result)

        cursor.close()
        conexion.close()

        if data:
            return {
                "status_code": status.HTTP_200_OK,
                "message": "List created successfully",
                "total": len(data_list),
                "data": data_list,
            }
        else:
            return {
                "status_code": status.HTTP_409_CONFLICT,
                "message": "No data in table simulation",
                "data": [],
            }
    except Exception as e:
        raise HTTPException(status_code=404, error=str(e))


@router.get(
    "/filter_simulations_by_status",
    status_code=status.HTTP_200_OK,
    responses={
        409: {"description": "..."},
        201: {"description": "Filter created sucessfully"},
    },
    name="filter_simulation_by_status",
    summary="list a table",
    description="This endpoint filter simulations by status from table simulation",
)
def filter_simulations_status(
    status_name: str = Query(..., description="status_name parameter"),
) -> []:
    try:
        conexion = get_conexion()
        cursor = conexion.cursor()

        # check if exists
        if not check_table_exists(TABLE_NAME.simulation, cursor):
            cursor.close()
            conexion.close()
            return {
                "status_code": status.HTTP_409_CONFLICT,
                "message": f"Table {TABLE_NAME.simulation} does not exist",
                "data": [],
            }

        query = f"""SELECT simulation.*
            FROM simulation
            JOIN status ON simulation.id_status = status.id_status
            WHERE status.status_name = '{status_name}';
        """

        cursor.execute(
            f"SELECT column_name FROM information_schema.columns WHERE table_name = '{TABLE_NAME.simulation}';"
        )
        columns = [column[0] for column in cursor.fetchall()]

        cursor.execute(query)
        data = cursor.fetchall()

        data_list = []
        for row in data:
            result = {}
            for idx, value in enumerate(row):
                result[columns[idx]] = value
            data_list.append(result)

        cursor.close()
        conexion.close()

        if data:
            return {
                "status_code": status.HTTP_200_OK,
                "message": "List created successfully",
                "status_name": status_name,
                "total": len(data_list),
                "data": data_list,
            }
        else:
            return {
                "status_code": status.HTTP_409_CONFLICT,
                "message": "No data in table simulation",
                "data": [],
            }
    except Exception as e:
        raise HTTPException(status_code=404, error=str(e))


@router.get(
    "/order_simulations",
    status_code=status.HTTP_200_OK,
    responses={
        409: {"description": "..."},
        201: {"description": "Filter created sucessfully"},
    },
    name="order_simulation",
    summary="list a table",
    description="This endpoint oder simulations",
)
def filter_simulations(
    order_by: Optional[str] = Query(
        None, description="order by simulation_code, created_at, or updated_at"
    ),
    sort: Optional[str] = Query(None, description="asc or desc parameter"),
) -> []:
    try:
        conexion = get_conexion()
        cursor = conexion.cursor()

        # check if exists
        if not check_table_exists(TABLE_NAME.simulation, cursor):
            cursor.close()
            conexion.close()
            return {
                "status_code": status.HTTP_409_CONFLICT,
                "message": f"Table {TABLE_NAME.simulation} does not exist",
                "data": [],
            }

        valid_order_fields = {"simulation_code", "created_at", "updated_at"}
        if order_by and order_by.lower() not in valid_order_fields:
            return {
                "message": "Invalid 'order_by' field. Use 'simulation_code', 'created_at', or 'updated_at'"
            }

        valid_form_fields = {"asc", "desc"}
        if sort and sort.lower() not in valid_form_fields:
            return {"message": "Invalid 'form' field. Use 'asc', 'desc'"}

        query = f"""SELECT simulation.*
            FROM simulation
            JOIN status ON simulation.id_status = status.id_status
            ORDER BY {order_by} {sort};
        """

        cursor.execute(
            f"SELECT column_name FROM information_schema.columns WHERE table_name = '{TABLE_NAME.simulation}';"
        )
        columns = [column[0] for column in cursor.fetchall()]

        cursor.execute(query)
        data = cursor.fetchall()

        data_list = []
        for row in data:
            result = {}
            for idx, value in enumerate(row):
                result[columns[idx]] = value
            data_list.append(result)

        cursor.close()
        conexion.close()

        if data:
            return {
                "status_code": status.HTTP_200_OK,
                "message": "List created successfully",
                "total": len(data_list),
                "order_by": order_by,
                "sort": sort,
                "data": data_list,
            }
        else:
            return {
                "status_code": status.HTTP_409_CONFLICT,
                "message": f"No ordered data in table {TABLE_NAME.simulation}",
                "data": [],
            }
    except Exception as e:
        raise HTTPException(status_code=404, error=str(e))


def insert_data(
    body,
) -> str:
    # we create FAKE data for the model
    total_duration_seconds = 12 * 60  # X minutes * X seconds
    interval_seconds = 2  # X-second interval

    simulation_data = [
        {"seconds": 5, "loss": 0.05},
    ]

    try:
        id_status = 1
        id_machine = body["machine_name"]
        id_model = body["model_name"]
        simulation_name = body["simulation_name"]

        created_at = datetime.now()
        updated_at = datetime.now()

        values = (
            id_status,
            id_machine,
            id_model,
            simulation_name,
            created_at,
            updated_at,
        )

        check_table = f"""
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_name = '{TABLE_NAME.simulation}'
            );
        """
        insert_data_simulation(
            INSERT_DATA_IN_TABLE.simulation,
            [values],
            check_table,
            TABLE_NAME.simulation,
        )

        # create fake data in the model for a simulation
        start_time = time.time()
        while (time.time() - start_time) < total_duration_seconds:
            seconds: int = simulation_data[-1]["seconds"] + 5

            base_loss = simulation_data[-1]["loss"]
            operation = random.choice([1, -1])
            random_change = random.uniform(0, 0.01)
            loss = base_loss + operation * random_change
            # loss: int = simulation_data[-1]["loss"] + 0.1

            new_data_point = {"seconds": seconds, "loss": loss}
            simulation_data.append(new_data_point)

            values = [(id_model, seconds, loss, "now()", "now()")]

            table_name = "data_model"
            check_table = f"""
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_name = '{table_name}'
                );
            """

            insert_data_model(
                INSERT_DATA_IN_TABLE.data_model, values, check_table, table_name
            )
            new_data_point = {"seconds": seconds, "loss": loss}

            logger.info(f"new record to post: {new_data_point}")
            time.sleep(interval_seconds)

        if (time.time() - start_time) > total_duration_seconds:
            return "data model for the simulation was created successfully, it's finished! \U0001F600"

    except Exception as e:
        raise HTTPException(status_code=404, error=str(e))


@router.post(
    "/create_simulation",
    status_code=status.HTTP_200_OK,
    responses={
        409: {"description": "..."},
        201: {"description": "Simulation created sucessfully"},
    },
    name="create_simulation",
    summary="create simulation",
    description="This endpoint create a simulation/model",
)
async def create_simulation(request: Request):
    body = await request.json()
    # wecreate task so as to not block others endpoints when POST is running
    loop = asyncio.get_event_loop()

    task = loop.run_in_executor(None, insert_data, body)
    message = await task

    return {"status_code": status.HTTP_200_OK, "message": message}
