"""Quote persistence and reporting."""

from app import billing


def _row_to_dict(row):
    return {key: row[key] for key in row.keys()}


def create_quote(conn, user_id, kwh, tariff_code, customer_type, promo=None):
    """Price and insert a quote, returning it as a dict."""
    price = billing.price_pence(kwh, tariff_code, customer_type, promo)
    cur = conn.execute(
        """
        INSERT INTO quotes (user_id, kwh, tariff_code, customer_type, promo, price_pence)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (user_id, kwh, tariff_code, customer_type, promo, price),
    )
    conn.commit()
    return get_quote(conn, cur.lastrowid)


def get_quote(conn, quote_id):
    row = conn.execute("SELECT * FROM quotes WHERE id = ?", (quote_id,)).fetchone()
    if row is None:
        return None
    return _row_to_dict(row)


def list_quotes(conn, user_id):
    rows = conn.execute(
        "SELECT * FROM quotes WHERE user_id = ? ORDER BY id", (user_id,)
    ).fetchall()
    return [_row_to_dict(row) for row in rows]


def report(conn):
    """Aggregate figures for the admin report endpoint."""
    row = conn.execute(
        "SELECT COUNT(*) AS count, COALESCE(SUM(price_pence), 0) AS total_pence FROM quotes"
    ).fetchone()
    by_tariff = {}
    for tariff_row in conn.execute(
        """
        SELECT tariff_code, COUNT(*) AS count, SUM(price_pence) AS total_pence
        FROM quotes GROUP BY tariff_code ORDER BY tariff_code
        """
    ).fetchall():
        by_tariff[tariff_row["tariff_code"]] = {
            "count": tariff_row["count"],
            "total_pence": tariff_row["total_pence"],
        }
    return {
        "count": row["count"],
        "total_pence": row["total_pence"],
        "by_tariff": by_tariff,
    }
