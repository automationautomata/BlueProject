import json
import time
from typing import Any, Self
import requests

from general.singleton import Singleton

# URL для запроса
def test():
    url = 'http://localhost:8080'

    try:
        # Отправка GET запроса
        response = requests.get(url)

        # Проверка статуса ответа
        if response.status_code == 200:
            print("Запрос успешен!")
            print("Ответ от сервера:", response.text)
        else:
            print(f"Ошибка {response.status_code}: {response.reason}")
    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при выполнении запроса: {e}")

from requests.auth import AuthBase

class TokenAuth(AuthBase):
    """Присоединяет HTTP аутентификацию к объекту запроса."""
    def __init__(self, token, id):
        # здесь настроем любые данные, связанные с аутентификацией 
        self.token = token
        self.id = id

    def __call__(self, req):
        # изменяем и возвращаем запрос
        if self.token:
            req.headers['X-Auth'] = self.token
            req.headers['X-Id'] = self.id
        return req
# while True:
#     time.sleep(0.5)
#     print(sd.get_table("entities", 0, "card", True))


class SkudApiRequsts(Singleton):
    def __init__(self, url: str) -> None:
        self.url = url
        self.token = None
        self.id = None

    def get(self, body: Any, path="") -> requests.Response | None:
        try:
            response = requests.get(self.url+path, data=body, auth=TokenAuth(self.token, self.id))
            if response.status_code == 200:
                return response
            else:
                print(f"Ошибка {response.status_code}: {response.reason}")
        except Exception as error:
            print("get ERR", error)

    def fmt(self, data) -> dict:
        return { "data"  : json.dumps(data)}
    
    def get_table(self, table: str, start: int, order_column: str, order_type: bool) -> dict | None:
        data = {"start"       : start, 
                "order_type"  : order_type, 
                "order_column": order_column}
 
        response = self.get(self.fmt(data), f"/ui/{table}")
        try: 
            return response.json()
        except Exception as error:
            print("response:", response.text if response else "None", 
                  "ERR:", error)
            
    def get_rights(self, getall=False):
        return self.get(self.fmt({"all": getall}), "/ui/rights")
    
    def authentication(self, key: int) -> tuple[bool, str]:
        data = json.dumps({"key": key, "id": self.id})
        response = self.get({"auth": data}, "/auth")
        try:
            answer = response.json()
            print(answer)

            err = "answer is None"
            if answer:
                err = answer["error"]
                if err == "":
                    self.token = answer["data"]
                    return True, err
            return False, err
        except BaseException as error:
            return False, error

api = SkudApiRequsts(url="http://localhost:8080")
print("url", api.url)
api.id = 2
while True:
    if input() == "auth":
        print("err, ", api.authentication(12))
    else:
        print("mmmm")
        print("req", api.get_rights())
        print("req", api.get_table("entities", 0, "card", False))
        print("ssss")
