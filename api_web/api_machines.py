import logging
from fastapi import APIRouter, HTTPException, status
from model.model import check_table_exists
from utils.conexion import HOST, DbPostgresManager
from utils.constants import TABLE_NAME
from utils.logging import apply_logging_conf

apply_logging_conf()
logger = logging.getLogger()


router = APIRouter(
    prefix="/v1.0",
    tags=["simulation"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/list_machines",
    status_code=status.HTTP_200_OK,
    responses={
        409: {"description": "..."},
        201: {"description": "List created sucessfully"},
    },
    name="list_machines",
    summary="list a table",
    description="This endpoint list machines from table machines",
)
def list_machines() -> []:
    try:
        query = """SELECT machines.* FROM machines;"""
        with DbPostgresManager(HOST, "db", "db", "db") as cursor:
            # check if exists
            if not check_table_exists(TABLE_NAME.machines, cursor):
                return {
                    "status_code": status.HTTP_409_CONFLICT,
                    "message": f"Table {TABLE_NAME.machines} does not exist",
                    "data": [],
                }

            cursor.execute(
                f"SELECT column_name FROM information_schema.columns WHERE table_name = '{TABLE_NAME.machines}';"
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

        if data:
            return {
                "status_code": status.HTTP_200_OK,
                "message": "List of models created successfully",
                "total": len(data_list),
                "data": data_list,
            }
        else:
            return {
                "status_code": status.HTTP_409_CONFLICT,
                "message": "No data in table model",
                "data": [],
            }
    except Exception as e:
        raise HTTPException(status_code=404, error=str(e))
