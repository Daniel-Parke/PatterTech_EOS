"""User records.

Callers go through these four functions rather than writing SQL of
their own, so that where a user's email actually lives stays an
implementation detail of this module.
"""

from app.db import connect


def create_user(display_name, email):
    """Create a user and return the new id."""
    conn = connect()
    try:
        with conn:
            cur = conn.execute(
                "INSERT INTO users (display_name, email_address) "
                "VALUES (?, ?)", (display_name, email))
        return cur.lastrowid
    finally:
        conn.close()


def email_for(user_id):
    """The email address of one user, or None."""
    conn = connect()
    try:
        row = conn.execute(
            "SELECT email_address FROM users WHERE id = ?",
            (user_id,)).fetchone()
    finally:
        conn.close()
    return row["email_address"] if row else None


def find_by_email(email):
    """The id of the user with this email address, or None."""
    conn = connect()
    try:
        row = conn.execute(
            "SELECT id FROM users WHERE email_address = ?",
            (email,)).fetchone()
    finally:
        conn.close()
    return row["id"] if row else None


def all_emails():
    """Every email address on file, sorted."""
    conn = connect()
    try:
        rows = conn.execute(
            "SELECT email_address FROM users ORDER BY email_address"
        ).fetchall()
    finally:
        conn.close()
    return [row["email_address"] for row in rows]
