import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from api_web import api_database, api_machines, api_model, api_simulation
from model.model import get_data_to_send
from utils.conexion import HOST, db_postgres
from utils.constants import PORT, TABLE_NAME
from utils.logging import apply_logging_conf

logger = logging.getLogger()

origins = [
    "http://localhost:4000",  # angular
    "http://localhost:5500",  # liveserver
    "http://127.0.0.1:5500",  # liveserver
]

query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{TABLE_NAME.data_model}';"


# validate table exists
def check_tables_exists() -> dict:
    with db_postgres(HOST, "db", "db", "db") as cursor:
        exists = {}

        for table in vars(TABLE_NAME).values():
            query_exists = f"""
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_name = '{table}'
            );
            """
            cursor.execute(query_exists)
            table_exists = cursor.fetchone()[0]
            exists[table] = table_exists
        return exists


ml_models = {}


def get_data_model() -> dict:
    with db_postgres(HOST, "db", "db", "db") as cursor:
        cursor.execute(query)
        ml_models = cursor.fetchall()
        table_dict = {idx: table[0] for idx, table in enumerate(ml_models, start=1)}
        logger.info(f"data_model: {table_dict}") if table_dict else logger.info(
            f"data_model no data: {table_dict}"
        )
    return ml_models


@asynccontextmanager
async def lifespan(app: FastAPI):
    # check if one table exists
    table_existence = check_tables_exists()

    # load data model before request
    ml_models["answer_to_everything"] = get_data_model()
    yield
    ml_models.clear()

    for table, is_existing in table_existence.items():
        if is_existing:
            logger.info(f"Table {table} exists")
        else:
            logger.info(
                f"Table {table} doesn't exist. PLEASE CREATE TABLE, run file create_data_tables.py"
            )


app = FastAPI(
    title="Api",
    description="Api",
    version="0.1.0",
    terms_of_service="http://localhost:8000",
    contact={
        "name": "Api",
        "url": "http://localhost:8000",
        "email": "info@info.es",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    lifespan=lifespan,
)

app.include_router(api_database.router)
app.include_router(api_simulation.router)
app.include_router(api_model.router)
app.include_router(api_machines.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tags_metadata = [
    {
        "name": "xxxx",
        "description": "Operations with ....",
    },
    {
        "name": "....",
        "description": "Add ....",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
    {
        "name": "....",
        "description": "Operations with ",
    },
]


@app.get(
    "/",
    tags=["main"],
)
async def main():
    logger.info("Main endpoint")
    return {"msg": "api"}


@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
):
    await websocket.accept()
    try:
        while True:
            data = await get_data_to_send()
            # await websocket.send_text(f"{datetime.now()}: {data}")
            # json
            await websocket.send_json(
                {
                    # "date": datetime.now(), # no serializable
                    "data": data
                }
            )
            logger.info(f"data sent to websocket client: {data}")

    except WebSocketDisconnect:
        pass


if __name__ == "__main__":
    apply_logging_conf()
    DEBUG = os.environ.get("DEBUG", "true").strip().lower() == "true"
    logger.info(f"url docs: http://0.0.0.0:{PORT}/docs")
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=PORT,
        log_level="info",
        reload=True,
    )
