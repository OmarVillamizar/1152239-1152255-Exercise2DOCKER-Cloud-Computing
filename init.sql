CREATE DATABASE notas;
\c notas;

CREATE TABLE notas (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    contenido TEXT
);