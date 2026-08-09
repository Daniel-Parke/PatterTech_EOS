"""HTTP entry points for the orders API.

The shapes here follow api/openapi.yaml. If you change one, change the
other in the same commit.
"""

from flask import Flask, jsonify, request

from app import store
from app.config import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from app.webhooks import bp as webhooks_bp


def error(code, message, field=None, status=400):
    body = {"code": code, "message": message}
    if field:
        body["field"] = field
    return jsonify(body), status


def create_app():
    app = Flask(__name__)
    app.register_blueprint(webhooks_bp)

    @app.post("/orders")
    def create_order():
        body = request.get_json(silent=True) or {}
        customer_id = body.get("customer_id")
        items = body.get("items") or []
        if not customer_id:
            return error("invalid_request", "customer_id is required",
                         field="customer_id")
        if not items:
            return error("invalid_request", "at least one item is required",
                         field="items")
        ref = body.get("ref")
        if ref and store.find_by_ref(ref):
            return error("duplicate_reference",
                         "an order with that reference already exists",
                         field="ref", status=409)
        order = store.create(customer_id, items, ref=ref)
        return jsonify(order), 201

    @app.get("/orders")
    def list_orders():
        try:
            limit = min(int(request.args.get("limit", DEFAULT_PAGE_SIZE)),
                        MAX_PAGE_SIZE)
            offset = int(request.args.get("offset", 0))
        except ValueError:
            return error("invalid_request",
                         "limit and offset must be whole numbers")
        status = request.args.get("status")
        rows, total = store.listing(status=status, limit=limit, offset=offset)
        return jsonify({
            "orders": rows,
            "total": total,
            "limit": limit,
            "offset": offset,
        })

    @app.get("/orders/<order_id>")
    def get_order(order_id):
        order = store.get(order_id)
        if order is None:
            return error("not_found", "no order with that id", status=404)
        return jsonify(order)

    return app


app = create_app()
