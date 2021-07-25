import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    from main import app

    with TestClient(app) as client:  # context manager will invoke startup event
        yield client


item_obj = {
    "name": "Harshit Singhai",
    "brand_name": "HS11",
    "regular_price_value": 38.5,
    "offer_price_value": 72.15,
    "currency": "GBP",
    "classification_l1": "sport & leisure",
    "classification_l2": "suitcases  bags & accessories",
    "classification_l3": "suitcases  bags & accessories-nch",
    "classification_l4": "",
    "image_url": "https://johnlewis.scene7.com/is/image/JohnLewis/237167637?",
}

item_id_lst = []


def test_get_items(client):
    response = client.get("/api/items")
    assert response.status_code == 200
    resp = response.json()
    assert len(resp) == 100


def test_get_item_by_id_not_found(client):
    # Check for invalid id
    response = client.get("/api/item/5001")
    assert response.status_code == 404


def test_create_item(client):
    response = client.post("/api/item", json=item_obj)
    assert response.status_code == 200
    item_id = response.json()["id"]

    item_id_lst.append(item_id)
    item_obj["id"] = item_id

    # Check if the obj is successfully created.
    response = client.get(f"/api/item/{item_id}")
    assert response.status_code == 200
    assert response.json() == item_obj

    # check if error is raise when required fields are missing
    item_obj_missing = item_obj.copy()
    del item_obj_missing["brand_name"]
    response = client.post("/api/item", json=item_obj_missing)
    assert response.status_code == 422

    # check when optional filds are missing
    item_obj_missing = item_obj.copy()
    del item_obj_missing["classification_l1"]
    del item_obj_missing["classification_l4"]
    response = client.post("/api/item", json=item_obj_missing)
    assert response.status_code == 200
    item_id_lst.append(response.json()["id"])


def test_get_item_by_id(client):
    item_id = item_id_lst[0]
    response = client.get(f"/api/item/{item_id}")
    assert response.status_code == 200
    assert response.json() == item_obj


def test_get_item_by_brand_name(client):
    response = client.get("/api/item/brand/betty & co.")
    assert response.status_code == 200
    assert len(response.json()) == 7

    response = client.get("/api/item/brand/gina bacconi")
    assert response.status_code == 200
    assert len(response.json()) == 12

    # Check error for invalid id
    response = client.get("/api/item/brand/random brand")
    assert response.status_code == 404


def test_update_item(client):
    item_id = item_id_lst[0]

    updated_item = {"regular_price_value": 48.5}
    response = client.patch(f"/api/item/{item_id}", json=updated_item)
    assert response.status_code == 200
    assert response.json()["regular_price_value"] == 48.5

    response = client.get(f"/api/item/{item_id}")
    assert response.status_code == 200
    assert response.json()["regular_price_value"] == updated_item["regular_price_value"]

    response = client.patch("/api/item/8912", json=updated_item)
    assert response.status_code == 404

    response = client.patch("/api/item/8912", json={})
    assert response.status_code == 404


def test_delete_item(client):
    for id in item_id_lst:
        response = client.delete(f"/api/item/{id}")
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["id"] == id

    # check if invalid item is deleted
    response = client.delete("/api/item/8712")
    assert response.status_code == 404


def test_count_discounted_products(client):
    response = client.get("/api/count_discounted_products")
    assert response.status_code == 200
    assert response.json()["count"]


def test_list_unique_brands(client):
    response = client.get("/api/list_unique_brands")
    assert response.status_code == 200
    assert response.json()["count_unique_brands"] == 539
    assert len(response.json()["unique_brands"]) == 539


def test_count_high_offer_price(client):
    response = client.get("/api/count_high_offer_price")
    assert response.status_code == 200
    assert response.json()["count"] == 214

    response = client.get("/api/count_high_offer_price?greater_than=500")
    assert response.status_code == 200
    assert response.json()["count"] == 87

    response = client.get("/api/count_high_offer_price?greater_than=10000")
    assert response.status_code == 404


def test_count_high_discount(client):
    response = client.get("/api/count_high_discount")
    assert response.status_code == 200
    assert response.json()["count"] == 717

    response = client.get("/api/count_high_discount?greater_than=70")
    assert response.status_code == 200
    assert response.json()["count"] == 41

    response = client.get("/api/count_high_discount?greater_than=120")
    assert response.status_code == 404
