import uuid
from types import SimpleNamespace

PORT = 8000
MODEL_NAME = "model_1"

TABLE_NAME = SimpleNamespace(
    simulation="simulation",
    status="status",
    model="model",
    machines="machines",
    data_model="data_model",
)

CREATE_TABLE = SimpleNamespace(
    simulation="""
        CREATE TABLE IF NOT EXISTS simulation (
            id_simulation SERIAL PRIMARY KEY,
            id_status INTEGER,
            id_machine INTEGER,
            id_model INTEGER,
            simulation_name VARCHAR(50) UNIQUE,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        );
    """,
    status="""
        CREATE TABLE IF NOT EXISTS status (
            id_status SERIAL PRIMARY KEY,
            status_name VARCHAR(50) UNIQUE,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        );
    """,
    machines="""
        CREATE TABLE IF NOT EXISTS machines (
            id_machines SERIAL PRIMARY KEY,
            machine_name VARCHAR(50) UNIQUE,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        );
    """,
    model="""
        CREATE TABLE IF NOT EXISTS model (
            id_model SERIAL PRIMARY KEY,
            model_name VARCHAR(50) UNIQUE,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        );
    """,
    data_model="""
        CREATE TABLE IF NOT EXISTS data_model (
            id SERIAL PRIMARY KEY,
            id_model INTEGER,
            seconds INTEGER,
            loss DECIMAL(5, 2),
            created_at TIMESTAMP,
            updated_at TIMESTAMP,
            CONSTRAINT fk_model
                FOREIGN KEY(id_model)
                REFERENCES model(id_model)
        );
    """,
)

INSERT_DATA_IN_TABLE = SimpleNamespace(
    status=(
        """
        INSERT INTO status(status_name, created_at, updated_at)
            VALUES(%s, %s, %s);
        """,
        [
            ("pending", "now()", "now()"),
            ("running", "now()", "now()"),
            ("finished", "now()", "now()"),
        ],
    ),
    simulation=(
        """
            INSERT INTO simulation(id_status, id_machine, id_model, simulation_name, created_at, updated_at)
            VALUES(%s, %s, %s, %s, %s, %s);
        """
    ),
    machines=(
        """
            INSERT INTO machines(machine_name, created_at, updated_at)
            VALUES(%s, %s, %s);
        """,
        [(str(uuid.uuid4()), "now()", "now()"), (str(uuid.uuid4()), "now()", "now()")],
    ),
    model=(
        """
            INSERT INTO model(model_name, created_at, updated_at)
            VALUES(%s, %s, %s);
        """,
        [
            (str(uuid.uuid4()), "now()", "now()"),
        ],
    ),
    data_model=(
        """
            INSERT INTO data_model(id_model, seconds, loss, created_at, updated_at)
            VALUES(%s, %s, %s, %s, %s);
        """
    ),
)
