from datetime import datetime
from typing import Any
import requests
import json

from singleton import Singleton


class SkudApiRequsts(Singleton):
    def __init__(self, url: str) -> None:
        self.url = url

    def get(self, body: Any) -> dict | None:
        try :
            response = requests.get(self.url, data=body)
            if response.status_code == 200:
                return json.loads(response.text)
            else:
                print(f"Ошибка {response.status_code}: {response.reason}")
        except NameError:
            print("get ERR", NameError)

    def fmt(self, action, data) -> dict:
        return {"action": action, "data": data, "token": self.token}
    
    def get_table(self, table: str, start: int, order_column: str, order_type: str) -> dict | None: 
        self.get(self.fmt(table + " query", 
                          {"start": start, "order_column": order_column, "order_type": order_type}))
        
    def authentication(self, key: int) -> tuple[bool, str]:
        answer = self.get(self.fmt("auth", {"key": key, "datetime": datetime.now().isoformat()}))
        
        err = "answer is None"
        if answer:
            err = answer["data"]["error"]
            if err == "":
                self.token = answer["data"]["token"]
                self.url += '/ui'
                return True, err
        return False, err