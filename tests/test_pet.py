from http.client import responses

import allure
import jsonschema
import pytest
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
                "id": 1,
                "name": "КОТ",
                "status": "available"
            }

        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response.json(), PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response.json()['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response.json()['name'] == payload['name'], "name питомца не совпадает с ожидаемым"
            assert response.json()['status'] == payload['status'], "status питомца не совпадает с ожидаемым"

    @allure.feature("Добавление нового питомца")
    def test_full_pet(self):
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

    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200
            assert response.json()["id"] == pet_id

    #@allure.title("удаление питомца")
    #def test_delete_pet_by_id(self, create_pet):
    #    pet_id = create_pet["id"]
    #    with allure.step(f"Удаляем питомца с ID = {pet_id}"):
    #        delete_response = requests.delete(f"{BASE_URL}/pet/{pet_id}")
    #        assert delete_response.status_code == 200

    #    with allure.step(f"Проверяем, что питомец с ID = {pet_id} удалён"):
    #        get_response = requests.get(f"{BASE_URL}/pet/{pet_id}")
    #        assert get_response.status_code == 404

    def test_update_pet(self, create_pet):
        pet_id = create_pet["id"]
        updated_data = {
            "id": 1,
            "name": "MAKS",
            "status": "available"
        }

        response = requests.put(f"{BASE_URL}/pet", json=updated_data)
        assert response.status_code == 200
        assert response.json()["name"] == "MAKS"

    def test_delete_pet(self, create_pet):
        pet_id = create_pet["id"]

        response = requests.delete(f"{BASE_URL}/pet/{pet_id}")
        assert response.status_code == 200

        # Проверка, что питомец удалён
        get_response = requests.get(f"{BASE_URL}/pet/{pet_id}")
        assert get_response.status_code == 404

        #  Урок 5

    @allure.title("Получение списка питомцев по статусу") #три положительных теста из урока
    @pytest.mark.parametrize(
        "status, expected_status_code",
        [
            ("available", 200),
            ("pending", 200),
            ("sold", 200)

        ]
    )
    def test_get_pets_by_status(self, status, expected_status_code):
        with allure.step("Отправка запроса на получение питомцев по статусу"):
            response = requests.get(f"{BASE_URL}/pet/findByStatus", params={"status": status})

        with allure.step("Проверка статуса ответа и формата данных"):
            assert response.status_code == 200
            assert isinstance(response.json(),list)

    @allure.title("Получение списка питомцев по статусу") #Добавлены три теста для задания
    @pytest.mark.parametrize(
        "status, expected_status_code",
        [
            ("no-no", 400),  # Некорректный статус — ожидаем 400
            ("", 400),  # Пустой статус — ожидаем 400
        ]
    )
    def test_get_pets_by_negative_status(self, status, expected_status_code):
        with allure.step("Отправка запроса на получение питомцев по статусу"):
            response = requests.get(f"{BASE_URL}/pet/findByStatus", params={"status": status})

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == expected_status_code

        if expected_status_code == 200:
            with allure.step("Проверка, что ответ содержит список питомцев"):
                assert isinstance(response.json(), list)
        else:
            with allure.step("Проверка, что тело ответа содержит ошибку"):
                assert response.text != ""