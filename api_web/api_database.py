import logging

from fastapi import APIRouter, HTTPException, status

from utils.conexion import get_conexion

logger = logging.getLogger()

router = APIRouter(
    prefix="/v1.0",
    tags=["database"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/list_tables",
    status_code=status.HTTP_200_OK,
    responses={
        409: {"description": "Tables already exists"},
        201: {"description": "Tables created sucessfully"},
    },
    name="list_tables",
    summary="list a table",
    description="This endpoint list all tables in the database",
)
async def list_tables() -> []:
    try:
        conexion = get_conexion()
        cursor = conexion.cursor()

        query = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE';
        """
        cursor.execute(query)
        tables = cursor.fetchall()
        table_dict = {idx: table[0] for idx, table in enumerate(tables, start=1)}
        logger.info(f"table_dict: {table_dict}")

        cursor.close()
        conexion.close()

        if tables:
            return {
                "status_code": status.HTTP_201_CREATED,
                "message": "Get all tables successfully",
                "data": table_dict,
            }
        else:
            return {
                "status_code": status.HTTP_409_CONFLICT,
                "message": "No tables in database",
                "data": [],
            }
    except Exception as e:
        raise HTTPException(status_code=404, error=str(e))
