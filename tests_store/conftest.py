# conftest.py
import pytest
import requests

BASE_URL = "http://5.181.109.28:9090/api/v3"

@pytest.fixture
def created_order():
    payload = {
        "id": 9876,
        "petId": 1,
        "quantity": 1,
        "status": "approved",
        "complete": True
    }

    response = requests.post(f"{BASE_URL}/store/order", json=payload)
    assert response.status_code == 200, "Не удалось создать заказ"
    yield payload["id"]
    requests.delete(f"{BASE_URL}/store/order/{payload['id']}")
