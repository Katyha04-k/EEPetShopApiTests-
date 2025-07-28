import allure
import requests
from datetime import datetime

BASE_URL = "https://petstore.swagger.io/v2"

@allure.feature("Store")
@allure.story("Создание заказа")
def test_create_order_success():

    order_payload = {
        "id": 99,
        "petId": 1,
        "quantity": 1,
        "status": "approved",
        "complete": True
    }

    with allure.step("Отправка POST-запроса на создание заказа"):
        response = requests.post(f"{BASE_URL}/store/order", json=order_payload)

    with allure.step("Проверка, что статус ответа равен 200"):
        assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}"

    with allure.step("Проверка содержимого ответа"):
        response_data = response.json()

        assert isinstance(response_data, dict), "Ответ должен быть в формате JSON (dict)"
        assert response_data.get("id") == order_payload["id"], "ID заказа не совпадает"
        assert response_data.get("petId") == order_payload["petId"], "ID питомца не совпадает"
        assert response_data.get("quantity") == order_payload["quantity"], "Количество не совпадает"
        assert response_data.get("status") == order_payload["status"], "Статус заказа не совпадает"
        assert response_data.get("complete") == order_payload["complete"], "Поле 'complete' не совпадает"


@allure.feature("Store")
@allure.story("Получение заказа по ID")
def test_get_order_by_id_success():
    order_id = 99

    with allure.step(f"Отправка GET-запроса на получение заказа с ID = {order_id}"):
        response = requests.get(f"{BASE_URL}/store/order/{order_id}")

    with allure.step("Проверка, что статус ответа равен 200"):
        assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}"

    with allure.step("Проверка содержимого ответа"):
        response_data = response.json()

        assert isinstance(response_data, dict), "Ответ должен быть в формате JSON (dict)"
        assert response_data.get("id") == order_id, f"ID заказа должен быть {order_id}"
        assert "petId" in response_data, "В ответе отсутствует поле petId"
        assert "quantity" in response_data, "В ответе отсутствует поле quantity"
        assert "status" in response_data, "В ответе отсутствует поле status"
        assert "complete" in response_data, "В ответе отсутствует поле complete"

@allure.feature("Store")
@allure.story("Удаление заказа по ID")
def test_delete_order_by_id_success():
    order_id = 99

    with allure.step(f"Отправка DELETE-запроса на удаление заказа с ID = {order_id}"):
        delete_response = requests.delete(f"{BASE_URL}/store/order/{order_id}")

    with allure.step("Проверка, что статус ответа на DELETE равен 200"):
        assert delete_response.status_code == 200, f"Ожидался статус 200, но получен {delete_response.status_code}"

    with allure.step(f"Отправка GET-запроса на получение удалённого заказа с ID = {order_id}"):
        get_response = requests.get(f"{BASE_URL}/store/order/{order_id}")

    with allure.step("Проверка, что заказ больше не существует (статус 404)"):
        assert get_response.status_code == 404, f"Ожидался статус 404, но получен {get_response.status_code}"

@allure.feature("Store")
@allure.story("Получение несуществующего заказа")
def test_get_nonexistent_order_returns_404():
    nonexistent_order_id = 9999  # Предполагаем, что такого заказа нет

    with allure.step(f"Отправка GET-запроса на получение несуществующего заказа с ID = {nonexistent_order_id}"):
        response = requests.get(f"{BASE_URL}/store/order/{nonexistent_order_id}")

    with allure.step("Проверка, что статус ответа равен 404"):
        assert response.status_code == 404, f"Ожидался статус 404, но получен {response.status_code}"

    with allure.step("Проверка содержимого ответа (опционально)"):
        if response.content:
            response_data = response.json()
            assert "message" in response_data, "В ответе ожидается поле 'message'"
            assert response_data["message"] in ["Order not found", "Not Found"], f"Неожиданное сообщение: {response_data['message']}"


@allure.feature("Store")
@allure.story("Получение инвентаря магазина")
def test_get_store_inventory_success():
    with allure.step("Отправка GET-запроса на /store/inventory"):
        response = requests.get(f"{BASE_URL}/store/inventory")

    with allure.step("Проверка, что статус ответа равен 200"):
        assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}"

    with allure.step("Проверка содержимого ответа"):
        response_data = response.json()
        assert isinstance(response_data, dict), "Ответ должен быть JSON-объектом (dict)"
        assert any(status in response_data for status in ["available", "pending", "sold"]), (
            "Инвентарь должен содержать хотя бы один из статусов: 'available', 'pending', 'sold'"
        )

        for key, value in response_data.items():
            assert isinstance(value, int), f"Значение для '{key}' должно быть числом, а не {type(value).__name__}"
