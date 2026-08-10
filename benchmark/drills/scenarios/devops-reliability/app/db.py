"""Database access.

One SQLite file, named by APP_DB so tests and CI can point at a
throwaway copy. Every query in the service goes through connect().
"""

import os
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "var" / "app.db"


def db_path():
    return Path(os.environ.get("APP_DB") or DEFAULT_DB)


def connect():
    path = db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
