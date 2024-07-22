DROP TABLE IF EXISTS users;

CREATE TABLE users(
    id        INTEGER      PRIMARY KEY AUTOINCREMENT,
    user_id   INTEGER UNIQUE NOT NULL,
    currency  TEXT         DEFAULT ₽ NOT NULL,
    join_date DATETIME     DEFAULT (DATETIME('now')) NOT NULL
);

INSERT INTO users(id, user_id, currency, join_date) VALUES (1, 123456789, '$', '2022-01-01 01:01:01');