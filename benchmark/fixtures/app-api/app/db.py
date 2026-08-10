"""SQLite helpers: connection, migrations, seed loading."""

import sqlite3
from datetime import datetime, timezone
from pathlib import Path


def connect(path):
    """Open a connection usable from the server's handler threads.

    check_same_thread is disabled because ThreadingHTTPServer handles each
    request on its own thread while sharing one connection. The server
    serialises access with a lock.
    """
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _ensure_migrations_table(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            filename TEXT PRIMARY KEY,
            applied_at TEXT NOT NULL
        )
        """
    )
    conn.commit()


def applied_migrations(conn):
    _ensure_migrations_table(conn)
    rows = conn.execute("SELECT filename FROM schema_migrations").fetchall()
    return {row["filename"] for row in rows}


def apply_migrations(conn, migrations_dir):
    """Apply every migrations/*.sql in sorted filename order, once each.

    Applied filenames are recorded in schema_migrations so re-running is a
    no-op. Returns the list of filenames applied on this call.
    """
    _ensure_migrations_table(conn)
    done = applied_migrations(conn)
    applied = []
    for sql_path in sorted(Path(migrations_dir).glob("*.sql")):
        name = sql_path.name
        if name in done:
            continue
        conn.executescript(sql_path.read_text(encoding="utf-8"))
        conn.execute(
            "INSERT INTO schema_migrations (filename, applied_at) VALUES (?, ?)",
            (name, datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()
        applied.append(name)
    return applied


def apply_sql_file(conn, path):
    """Execute a plain SQL file, used for seed data."""
    conn.executescript(Path(path).read_text(encoding="utf-8"))
    conn.commit()
