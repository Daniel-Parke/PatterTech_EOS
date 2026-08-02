"""User accounts and bearer tokens.

Passwords are stored as sha256 hex digests. Tokens live in an in-memory
store, so a restart signs everyone out. Both are deliberate simplifications
for a fixture; neither is the planted defect.
"""

import hashlib
import secrets

# token -> {"user_id": int, "email": str, "role": str}
_TOKENS = {}


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_user(conn, email, password, role="user"):
    """Insert a user and return its id. Raises sqlite3.IntegrityError on
    duplicate email or an unknown role."""
    cur = conn.execute(
        "INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)",
        (email, hash_password(password), role),
    )
    conn.commit()
    return cur.lastrowid


def issue_token(conn, email, password):
    """Return a fresh token for valid credentials, otherwise None."""
    row = conn.execute(
        "SELECT id, email, password_hash, role FROM users WHERE email = ?",
        (email,),
    ).fetchone()
    if row is None:
        return None
    if row["password_hash"] != hash_password(password):
        return None
    token = secrets.token_hex(16)
    _TOKENS[token] = {"user_id": row["id"], "email": row["email"], "role": row["role"]}
    return token


def check_token(token):
    """Return the claims dict for a live token, otherwise None."""
    if not token:
        return None
    return _TOKENS.get(token)


def revoke_token(token):
    _TOKENS.pop(token, None)


def clear_tokens():
    _TOKENS.clear()
