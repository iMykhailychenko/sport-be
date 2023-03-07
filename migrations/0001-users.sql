CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    password VARCHAR(128) NOT NULL,
    email character varying(254) NOT NULL UNIQUE
);