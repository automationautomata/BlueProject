CREATE TABLE cards (
    id VARCHAR(4) PRIMARY KEY,
    isSabotaged VARCHAR(1) NOT NULL
    date_time TEXT NOT NULL
);
CREATE TABLE rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
    date_time TEXT NOT NULL
);
CREATE TABLE rights (
    id INTEGER NOT NULL AUTOINCREMENT,
    name TEXT NOT NULL
    date_time TEXT NOT NULL
);
CREATE TABLE access_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    right INTEGER NOT NULL,
    room INTEGER NOT NULL,
    FOREIGN KEY(room) REFERENCES rooms(id),
    FOREIGN KEY(right) REFERENCES rights(id)
    UNIQUE(right, room)
    date_time TEXT NOT NULL
);
CREATE TABLE entities (
    card VARCHAR(4),
    sid INTEGER PRIMARY KEY,
    type VARCHAR(1) NOT NULL,
    right INTEGER NOT NULL,
    FOREIGN KEY(card) REFERENCES cards(id),
    FOREIGN KEY(right) REFERENCES rights(id)
    date_time TEXT NOT NULL
);