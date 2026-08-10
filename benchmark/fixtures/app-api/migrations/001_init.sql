CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user' CHECK (role IN ('user', 'admin')),
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    kwh INTEGER NOT NULL,
    tariff_code TEXT NOT NULL,
    customer_type TEXT NOT NULL,
    promo TEXT,
    price_pence INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
