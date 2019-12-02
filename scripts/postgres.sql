CREATE TABLE IF NOT EXISTS users (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(40) NOT NULL,
    is_active   BOOLEAN NOT NULL,
    created_at  DATE NOT NULL DEFAULT CURRENT_DATE
);
