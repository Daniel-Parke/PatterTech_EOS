"""Boot the quote API: migrate, seed when empty, serve on 127.0.0.1:8765."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from app import db, server  # noqa: E402

HOST = "127.0.0.1"
PORT = 8765


def main():
    data_dir = ROOT / "data"
    data_dir.mkdir(exist_ok=True)
    conn = db.connect(str(data_dir / "app.db"))
    db.apply_migrations(conn, str(ROOT / "migrations"))
    user_count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if user_count == 0:
        db.apply_sql_file(conn, str(data_dir / "seed.sql"))
    srv = server.create_server(conn, HOST, PORT)
    print("Quote API listening on http://{}:{}".format(HOST, PORT))
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.shutdown()


if __name__ == "__main__":
    main()
