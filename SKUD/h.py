import json
import time
from typing import Any, Self
import requests

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


class SkudHttpRequsts:
    _instance: Self = None
    def __new__(class_, **kwargs) -> str:
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_)
            class_._instance.url = kwargs['url']
        return class_._instance
    
    def get(self, json_body: dict) -> str:
        '''Отправляет запрос и возвращает ответ'''
        try :
            response = requests.get(self.url, data=json_body)
            if response.status_code == 200:
                print(response.text)
                return response.text
            else:
                print(f"Ошибка {response.status_code}: {response.reason}")
        except NameError:
            print("get ERR", NameError)
    
    def get_table(self, table: str, start, order_column, order_type) -> dict[str, Any]: 
        res = self.get({"action": table + " query", 
                         "data": json.dumps({"start": start, "order_column": order_column, 
                                             "order_type": order_type})})
        return json.loads(res) if res else None
    
    def get_sorted(self, table: str, sorting_rules: dict[str, str]) -> dict[str, Any]: 
        res =  self.get({"action": table + " sorted", "data": json.dumps(sorting_rules)})
        return json.loads(res) if res else None

sd = SkudHttpRequsts(url='http://localhost:8080')
while True:
    time.sleep(0.5)
    print(sd.get_table("entities", 0, "card", True))
