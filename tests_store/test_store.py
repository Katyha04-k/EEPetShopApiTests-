# tests/test_store.py
import requests
import allure
from jsonschema import validate
from tests.schemas.store_schema import STORE_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Store")
@allure.story("Создание заказа")
def test_create_order_success():
    order_payload = {
        "id": 9999,
        "petId": 1,
        "quantity": 2,
        "status": "approved",
        "complete": True
    }

    with allure.step("Отправка POST-запроса на создание заказа"):
        response = requests.post(f"{BASE_URL}/store/order", json=order_payload)

    with allure.step("Проверка, что статус ответа равен 200"):
        assert response.status_code == 200

    with allure.step("Проверка содержимого ответа и схемы"):
        response_data = response.json()
        validate(instance=response_data, schema=STORE_SCHEMA)

        assert response_data["id"] == order_payload["id"]
        assert response_data["petId"] == order_payload["petId"]
        assert response_data["quantity"] == order_payload["quantity"]
        assert response_data["status"] == order_payload["status"]
        assert response_data["complete"] == order_payload["complete"]


@allure.feature("Store")
@allure.story("Получение заказа по ID")
def test_get_order_by_id_success(created_order):
    order_id = created_order

    with allure.step(f"Запрос GET для заказа ID={order_id}"):
        response = requests.get(f"{BASE_URL}/store/order/{order_id}")
        assert response.status_code == 200
        response_data = response.json()

    with allure.step("Валидация схемы и содержимого"):
        validate(instance=response_data, schema=STORE_SCHEMA)
        assert response_data["id"] == order_id

@allure.feature("Store")
@allure.story("Удаление заказа по ID")
def test_delete_order_by_id_success(created_order):
    order_id = created_order

    with allure.step(f"Удаление заказа ID={order_id}"):
        delete_response = requests.delete(f"{BASE_URL}/store/order/{order_id}")
        assert delete_response.status_code == 200

    with allure.step("Проверка, что заказ больше не существует"):
        get_response = requests.get(f"{BASE_URL}/store/order/{order_id}")
        assert get_response.status_code == 404


@allure.feature("Store")
@allure.story("Получение несуществующего заказа")
def test_get_nonexistent_order_returns_404():
    invalid_id = 123456789

    with allure.step(f"GET-запрос на несуществующий ID={invalid_id}"):
        response = requests.get(f"{BASE_URL}/store/order/{invalid_id}")
        assert response.status_code == 404

    with allure.step("Проверка, что ответ — не JSON"):
        try:
            response_data = response.json()
        except requests.exceptions.JSONDecodeError:
            response_data = {}

        if response_data:
            assert "message" in response_data
            assert response_data["message"] in ["Order not found", "Not Found"]


@allure.feature("Store")
@allure.story("Получение инвентаря магазина")
def test_get_store_inventory_success():
    with allure.step("GET-запрос на /store/inventory"):
        response = requests.get(f"{BASE_URL}/store/inventory")
        assert response.status_code == 200

    with allure.step("Проверка содержимого инвентаря"):
        data = response.json()
        assert isinstance(data, dict)
    for key, value in data.items():
        assert isinstance(value, int)