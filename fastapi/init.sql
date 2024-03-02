CREATE TABLE IF NOT EXISTS clients (
    "id"                SERIAL,
    "limite"            INT NOT NULL,
    "saldo"             INT NOT NULL,

    PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS transactions (
    "id"             SERIAL,
    "valor"          INT NOT NULL,
    "tipo"           VARCHAR(1) NOT NULL,
    "descricao"      VARCHAR(10) NOT NULL,
    "realizada_em"   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    "client_id"      INT NOT NULL,

    PRIMARY KEY (id),
    CONSTRAINT "clients_fk" FOREIGN KEY ("client_id") REFERENCES clients("id")
);


DO $$
BEGIN
  INSERT INTO clients ("id", "limite", "saldo")
  VALUES
    (1, 100000, 0),
    (2, 80000, 0),
    (3, 1000000, 0),
    (4, 10000000, 0),
    (5, 500000, 0);
END; $$
