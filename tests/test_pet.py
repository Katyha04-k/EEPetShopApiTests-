from http.client import responses

import allure
import jsonschema
import requests
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Pet")
class TestPet:
    @allure.feature("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"

    @allure.feature("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }
            response = requests.put( url=f"{BASE_URL}/pet", json=payload)

            with allure.step("Проверка статуса ответа"):
                assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

            with allure.step("Проверка текстового содержимого ответа"):
                assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.feature("Попытка получить информацию о несуществующем питомце")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на получение информации о несуществующем питомце"):
            response = requests.get(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.feature("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {
                    "id": 1,
                    "name": "Dogs"
                },
                "photoUrls": [
                    "string"
                ],
                "tags": [
                    {
                        "id": 0,
                        "name": "string"
                    }
                ],
                "status": "available"
            }

        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
                assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
                jsonschema.validate(response.json(),PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response.json()['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response.json()['name'] == payload['name'], "name питомца не совпадает с ожидаемым"
            assert response.json()['status'] == payload['status'], "status питомца не совпадает с ожидаемым"
            assert response.json()['category'] == payload['category'], "категория питомца не совпадает с ожидаемым"
            assert response.json()['photoUrls'] == payload['photoUrls'], "photoUrls питомца не совпадает с ожидаемым"
            assert response.json()['tags'] == payload['tags'], "tags питомца не совпадает с ожидаемым"