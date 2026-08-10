-- Users, one row per person who can sign in.

CREATE TABLE users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    display_name  TEXT NOT NULL,
    email_address TEXT NOT NULL,
    created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE UNIQUE INDEX users_email_address_idx ON users (email_address);
