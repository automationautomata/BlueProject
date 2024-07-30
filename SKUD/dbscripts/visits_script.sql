CREATE TABLE visits_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    port TEXT NOT NULL,
    message TEXT NOT NULL,
    pass_time TEXT NOT NULL
);
CREATE TABLE remote_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    address TEXT NOT NULL,
    event TEXT NOT NULL,
    date_time TEXT NOT NULL
);