import sqlite3 as sqlite
from ORM.database import DatabaseConnection
import os 
from datetime import datetime
from itertools import product

class Logger(DatabaseConnection):
    __scriptpath = "SKUD\\loggerscript.sql"
    def __init__(self, name: str, dirpath: str = "./") -> None:
        super().__init__(Logger.__scriptpath, name, dirpath)

    def establish_connection(self) -> None:
        '''Устанавливает соединение c базой и, если БД отсутствует,
        то пересоздает ее на основе указанного скрипта.'''
        path = f"{self.__dirpath}{self.__name}"
        if not os.path.isfile(path):
            self._createdatabase_(Logger.__scriptpath)
        self._connection_ = sqlite.connect(path)
    
    def addlog(self, messages: list[str]):
        cursor = self._connection_.cursor()
        sql = "INSERT INTO projects(message, time) VALUES(?,?)"
        time = datetime.now().isoformat()
        return cursor.execute(sql, list(product(messages, [time])))