-- Table: usuarios 
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Assuming auto-incrementing ID
    email VARCHAR(255) UNIQUE NOT NULL,  -- String type, change size as needed
    name VARCHAR(255), 
    password VARCHAR(255),
    cpf VARCHAR(255) UNIQUE, -- String type, adjust if needed for CPF format
);

-- Table: sessoes
CREATE TABLE sessoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chave VARCHAR(255) UNIQUE,
    usuario_id INTEGER NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)  
);

-- Table: aeroportos
CREATE TABLE aeroportos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) UNIQUE,
    city VARCHAR(255) 
);

-- Table: voos 
CREATE TABLE voos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    origin_id INTEGER NOT NULL,
    destination_id INTEGER NOT NULL,
    origin_city VARCHAR(255), 
    destination_city VARCHAR(255), 
    departure_date DATE,
    price INTEGER,
    available_tickets INTEGER,

    FOREIGN KEY (origem_id) REFERENCES aeroportos(id),
    FOREIGN KEY (destination_id) REFERENCES aeroportos(id),
);

-- Table: ticket
CREATE TABLE ticket (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,
    e_ticket VARCHAR(255) UNIQUE,
    FOREIGN KEY (flight_id) REFERENCES voos(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

