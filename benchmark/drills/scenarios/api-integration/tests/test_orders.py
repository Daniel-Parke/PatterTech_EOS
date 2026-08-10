import pytest

from app import store
from app.main import create_app


@pytest.fixture()
def client():
    store.clear()
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def a_line(sku="SKU-1", quantity=2, price=650):
    return {"sku": sku, "quantity": quantity, "unit_price_pence": price}


def test_create_order_returns_the_created_order(client):
    response = client.post("/orders", json={
        "customer_id": "5b7c0f9e-7b1f-4a2e-9a55-1c3f0c9f2e11",
        "items": [a_line()],
    })
    assert response.status_code == 201
    body = response.get_json()
    assert body["status"] == "pending"
    assert body["total_pence"] == 1300
    assert body["ref"].startswith("ORD-")


def test_create_order_rejects_a_missing_customer(client):
    response = client.post("/orders", json={"items": [a_line()]})
    assert response.status_code == 400
    assert response.get_json()["field"] == "customer_id"


def test_duplicate_reference_is_a_conflict(client):
    body = {
        "customer_id": "5b7c0f9e-7b1f-4a2e-9a55-1c3f0c9f2e11",
        "items": [a_line()],
        "ref": "ORD-90001",
    }
    assert client.post("/orders", json=body).status_code == 201
    assert client.post("/orders", json=body).status_code == 409


def test_listing_pages_with_limit_and_offset(client):
    for i in range(5):
        client.post("/orders", json={
            "customer_id": "5b7c0f9e-7b1f-4a2e-9a55-1c3f0c9f2e11",
            "items": [a_line(sku="SKU-%d" % i)],
        })
    page = client.get("/orders?limit=2&offset=2").get_json()
    assert page["total"] == 5
    assert len(page["orders"]) == 2
    assert page["offset"] == 2
