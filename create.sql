create table simulation (
    id_simulation serial,
    id_status integer,
    id_machine integer,
    id_model integer,
    simulation_code varchar(50),
    created_at timestamp,
    updated_at timestamp,
    PRIMARY KEY(id_simulation),
    CONSTRAINT fk_model
        FOREIGN KEY(id_model)
            REFERENCES model(id_model)
);

create table status (
    id_status serial primary key,
    status_name varchar(50),
    created_at timestamp,
    updated_at timestamp,
);

create table machines (
    id_machines serial primary key,
    id_simulation integer,
    machine_name varchar(50),
    created_at timestamp,
    updated_at timestamp,
);

create table model (
    id_model serial primary key,
    model_name varchar(50),
    created_at timestamp,
    updated_at timestamp
);

create table data_model (
    id_data SERIAL PRIMARY KEY,
    id_model INTEGER,
    seconds INTEGER,
    loss DECIMAL(5, 2),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    CONSTRAINT fk_model
        FOREIGN KEY(id_model)
        REFERENCES simulation(id_model)
);

INSERT INTO status(status_name, created_at, updated_at)
VALUES('pending', now(), now()),
        ('runnign', now(), now()),
        ('finished', now(), now());

INSERT INTO simulation(simulation_code, id_status, created_at, updated_at)
VALUES('simulation_1', 1, now(), now()),
        ('simulation_2', 2, now(), now()),
        ('simulation_3', 3, now(), now());

INSERT INTO machines(machine_name, created_at, updated_at)
VALUES('machine_1', now(), now()),
        ('machine_2', now(), now()),
        ('machine_3', now(), now());

