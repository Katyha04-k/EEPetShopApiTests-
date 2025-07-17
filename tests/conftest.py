import pytest
import requests

BASE_URL = "http://5.181.109.28:9090/api/v3"

@pytest.fixture(scope="function")
def create_pet():
    """Фикстура для создания питомца"""
    payload = {
        "id": 1,
        "name": "КОТ",
        "status": "available"
    }
    response = requests.post(url=f"{BASE_URL}/pet", json=payload)
    assert response.status_code == 200
    return response.json()

#@pytest.fixture(scope="function")
#def update_pet():
#    """Фикстура для обновления информации о питомце"""
#    payload = {
#        "id": 10,
#        "name": "doggie",
#        "category": {
#            "id": 111,
#            "name": "КОТ"
#        },
#        "photoUrls": [
#            "string"
#        ],
#        "tags": [
#            {
#                "id": 0,
#                "name": "string"
#            }
#        ],
#        "status": "available"
#    }
#    response = requests.put(url=f"{BASE_URL}/pet", json=payload)
#    assert response.status_code == 200
#    return response.json()

#@pytest.fixture(scope="function")
#def delete_pet(update_pet):
#    """Фикстура для удаления информации о питомце, созданного через update_pet"""
#    pet_id = update_pet ["id"]
#    response = requests.delete(url=f"{BASE_URL}/pet/{pet_id}")
#    assert response.status_code == 200 or response.status_code == 404
#    return response