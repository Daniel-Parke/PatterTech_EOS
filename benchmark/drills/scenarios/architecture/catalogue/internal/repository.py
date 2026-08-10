"""Storage detail. Off limits to anything outside the catalogue."""

_PRODUCTS = {
    "seat": {"id": "seat", "name": "Seat", "list_price": 12.00},
    "audit": {"id": "audit", "name": "Audit", "list_price": 480.00},
}


def load(product_id):
    return _PRODUCTS.get(product_id)


def load_all():
    return list(_PRODUCTS.values())
