import json

import pytest

from app import store
from app.config import WEBHOOK_TOKEN
from app.main import create_app


@pytest.fixture()
def client():
    store.clear()
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def an_order(client):
    return client.post("/orders", json={
        "customer_id": "5b7c0f9e-7b1f-4a2e-9a55-1c3f0c9f2e11",
        "items": [{"sku": "SKU-1", "quantity": 1, "unit_price_pence": 500}],
    }).get_json()


def test_settled_charge_marks_the_order_paid(client):
    order = an_order(client)
    response = client.post(
        "/webhooks/payments",
        data=json.dumps({"id": "evt_1", "type": "charge.settled",
                         "order_id": order["id"]}),
        headers={"X-Webhook-Token": WEBHOOK_TOKEN,
                 "Content-Type": "application/json"},
    )
    assert response.status_code == 204
    assert store.get(order["id"])["status"] == "paid"


def test_a_wrong_token_is_rejected(client):
    order = an_order(client)
    response = client.post(
        "/webhooks/payments",
        data=json.dumps({"id": "evt_2", "type": "charge.settled",
                         "order_id": order["id"]}),
        headers={"X-Webhook-Token": "not-the-token",
                 "Content-Type": "application/json"},
    )
    assert response.status_code == 401
    assert store.get(order["id"])["status"] == "pending"


def test_an_unknown_event_type_is_a_bad_request(client):
    response = client.post(
        "/webhooks/payments",
        data=json.dumps({"id": "evt_3", "type": "charge.exploded",
                         "order_id": "does-not-matter"}),
        headers={"X-Webhook-Token": WEBHOOK_TOKEN,
                 "Content-Type": "application/json"},
    )
    assert response.status_code == 400
