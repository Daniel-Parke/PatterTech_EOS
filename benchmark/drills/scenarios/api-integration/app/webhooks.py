"""Payment events posted to us by the payment provider.

The provider retries a 5xx for up to a day, so this handler answers
quickly and does the work inline. It is small enough for that to be
fine.
"""

import json
import logging

from flask import Blueprint, jsonify, request

from app import store
from app.config import WEBHOOK_TOKEN

log = logging.getLogger(__name__)

bp = Blueprint("webhooks", __name__)

STATUS_FOR_EVENT = {
    "charge.settled": "paid",
    "charge.failed": "pending",
    "charge.refunded": "cancelled",
}


@bp.post("/webhooks/payments")
def receive_payment_event():
    event = json.loads(request.get_data() or b"{}")

    token = request.headers.get("X-Webhook-Token", "")
    if token != WEBHOOK_TOKEN:
        log.warning("rejected event %s: token did not match", event.get("id"))
        return jsonify({"code": "unauthorised",
                        "message": "the shared token did not match"}), 401

    event_type = event.get("type")
    order_id = event.get("order_id")
    if event_type not in STATUS_FOR_EVENT or not order_id:
        return jsonify({"code": "invalid_event",
                        "message": "unknown event type or missing order"}), 400

    order = store.set_status(order_id, STATUS_FOR_EVENT[event_type])
    if order is None:
        log.info("event %s is for order %s, which we do not have",
                 event.get("id"), order_id)
    return "", 204
