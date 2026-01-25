import allure
import jsonschema
import requests
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            responce = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert responce.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert responce.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }
            responce = requests.put(url=f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа"):
            assert responce.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert responce.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_get_inf_nonexistent_pet(self):
        with allure.step("Отправка запроса на поучение информации о несуществующем питомце"):
            responce = requests.get(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert responce.status_code == 404, "Код ответа не совпал с ожидаемым"

    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }
        with allure.step("Отправка запроса на создание питомца"):
            responce = requests.post(url=f"{BASE_URL}/pet", json=payload)
            responce_json = responce.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert responce.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(responce_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert responce_json['id'] == payload['id'], "id питомца не совпал с ожидаемым"
            assert responce_json['name'] == payload['name'], "name питомца не совпал с ожидаемым"
            assert responce_json['status'] == payload['status'], "status не совпал с ожидаемым"

    @allure.title("Добавление нового питомца с полными данными")
    def test_add_pet_new(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {
                    "id": 1,
                    "name": "Dogs"
                },
                "photoUrls": ["string"],
                "tags": [{
                    "id": 0,
                    "name": "string"
                }],
                "status": "available"
            }
        with allure.step("Отправка запроса на создание питомца с полными данными"):
            responce = requests.post(url=f"{BASE_URL}/pet", json=payload)
            responce_json = responce.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert responce.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(responce_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert responce_json['id'] == payload['id'], "id питомца не совпал с ожидаемым"
            assert responce_json['name'] == payload['name'], "name питомца не совпало с ожидаемым"
            assert responce_json['category'] == payload['category'], "category питомца не совпала с ожидаемой"
            assert responce_json['photoUrls'] == payload['photoUrls'], "photoUrls не совпал с ожидаемым"
            assert responce_json['tags'] == payload['tags'], "tags не совпал с ожидаемым"
            assert responce_json['status'] == payload['status'], "status не совпал с ожидаемым"
