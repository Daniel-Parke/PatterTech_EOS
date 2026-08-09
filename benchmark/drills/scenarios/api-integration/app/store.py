"""In-memory order store.

Good enough while the service is single process. Everything here is
keyed by order id and kept in insertion order, newest last.
"""

import itertools
import uuid
from datetime import datetime, timezone

_ORDERS = {}
_COUNTER = itertools.count(24001)


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def create(customer_id, items, ref=None):
    order_id = str(uuid.uuid4())
    order = {
        "id": order_id,
        "ref": ref or "ORD-%d" % next(_COUNTER),
        "customer_id": customer_id,
        "status": "pending",
        "total_pence": sum(i["quantity"] * i["unit_price_pence"]
                           for i in items),
        "created_at": _now(),
        "items": list(items),
    }
    _ORDERS[order_id] = order
    return order


def get(order_id):
    return _ORDERS.get(order_id)


def find_by_ref(ref):
    for order in _ORDERS.values():
        if order["ref"] == ref:
            return order
    return None


def listing(status=None, limit=25, offset=0):
    """A page of orders, newest first, with the total behind the filter."""
    rows = list(reversed(list(_ORDERS.values())))
    if status:
        rows = [o for o in rows if o["status"] == status]
    return rows[offset:offset + limit], len(rows)


def set_status(order_id, status):
    order = _ORDERS.get(order_id)
    if order is None:
        return None
    order["status"] = status
    return order


def clear():
    _ORDERS.clear()
