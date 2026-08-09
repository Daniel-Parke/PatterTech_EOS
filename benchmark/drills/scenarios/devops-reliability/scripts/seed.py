#!/usr/bin/env python3
"""Put the standing sample users into the database.

    python scripts/seed.py

The same twelve people every time, so a local database and a CI
database hold the same rows and a diff of the two means something.
Safe to run twice.
"""

import os
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PEOPLE = [
    ("Ada Lovelace", "ada.lovelace@example.com", "referral"),
    ("Grace Hopper", "grace.hopper@example.com", "organic"),
    ("Alan Turing", "alan.turing@example.com", "organic"),
    ("Katherine Johnson", "katherine.johnson@example.com", "referral"),
    ("Edsger Dijkstra", "edsger.dijkstra@example.com", "campaign"),
    ("Barbara Liskov", "barbara.liskov@example.com", "organic"),
    ("Tony Hoare", "tony.hoare@example.com", "campaign"),
    ("Margaret Hamilton", "margaret.hamilton@example.com", "referral"),
    ("Donald Knuth", "donald.knuth@example.com", "organic"),
    ("Radia Perlman", "radia.perlman@example.com", "campaign"),
    ("Leslie Lamport", "leslie.lamport@example.com", "organic"),
    ("Karen Sparck Jones", "karen.sparck.jones@example.com", "referral"),
]


def db_path():
    return Path(os.environ.get("APP_DB") or ROOT / "var" / "app.db")


def main():
    path = db_path()
    if not path.is_file():
        sys.exit("no database at %s; run scripts/migrate.py first" % path)
    conn = sqlite3.connect(str(path))
    try:
        with conn:
            for name, email, source in PEOPLE:
                conn.execute(
                    "INSERT OR IGNORE INTO users "
                    "(display_name, email_address) VALUES (?, ?)",
                    (name, email))
        count = conn.execute("SELECT count(*) FROM users").fetchone()[0]
    finally:
        conn.close()
    print("seeded, %d users on file" % count)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
