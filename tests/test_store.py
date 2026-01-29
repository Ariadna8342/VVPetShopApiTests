import allure
import requests
import jsonschema
from .schemas.store_schema import STORE_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа")
    def test_new_order(self):
        with allure.step("Отправка запроса на размещение заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }

            response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка параметров заказа в ответе"):
            assert response_json['id'] == payload['id'], "id заказа не совпал с ожидаемым"
            assert response_json['petId'] == payload['petId'], "petId питомца не совпал с ожидаемым"
            assert response_json['quantity'] == payload['quantity'], "количество не совпало с ожидаемым"
            assert response_json['status'] == payload['status'], "status не совпал с ожидаемым"
            assert response_json['complete'] == payload['complete'], "комлектация не совпала с ожидаемой"

    @allure.title("Получение информации о заказе по Id")
    def test_get_info_by_order(self, create_order):
        with allure.step("Получение ID размещенного заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(f"{BASE_URL}/store/order/{order_id}")
            response_json = response.json()

        with allure.step("Проверка статуса ответа и данных заказа"):
            assert response.status_code == 200

            assert response_json["id"] == order_id
            assert response_json["petId"] == create_order["petId"]
            assert response_json["quantity"] == create_order["quantity"]
            assert response_json["status"] == create_order["status"]
            assert response_json["complete"] == create_order["complete"]

    @allure.title("Удаление заказа по ID")
    def test_delete_order_by_id(self, create_order):
        with allure.step("Получение ID размещенного заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка запроса на удаление заказа по ID"):
            response = requests.delete(url=f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Отправка запроса на получение заказа по ID"):
            response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_nonexistent_order(self):
        with allure.step("Отправка запроса на получение информации о несуществующем заказе"):
            response = requests.get(url=f"{BASE_URL}/store/order/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

    @allure.title("Получение инвентаря магазина")
    def test_get_inventory_of_shop(self):
        with allure.step("Отправка запроса на получение инвентаря магазина"):
            response = requests.get(url=f"{BASE_URL}/store/inventory")
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация формата ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым "
            jsonschema.validate(response_json, STORE_SCHEMA)


