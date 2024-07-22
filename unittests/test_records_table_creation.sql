DROP TABLE IF EXISTS records;

CREATE TABLE records(
    id        INTEGER  PRIMARY KEY AUTOINCREMENT,
    users_id  INTEGER  REFERENCES users (id) ON DELETE CASCADE NOT NULL,
    category  TEXT NOT NULL,
    operation BOOLEAN  NOT NULL,
    value     DECIMAL  NOT NULL,
    date      DATETIME DEFAULT (DATETIME('now')) NOT NULL
);

INSERT INTO records(id, users_id, category, operation, value, date) VALUES (1, 1, '📚 Education', 1, 10000, '2022-01-01 01:01:01');
