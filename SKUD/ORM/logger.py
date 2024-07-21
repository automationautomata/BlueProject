import sqlite3 as sqlite
from ORM.database import DatabaseConnection
import os 
import datetime
from itertools import product

class Logger(DatabaseConnection):
    def __init__(self, name: str) -> None:
        '''name - название БД.'''
        self.__name = name

    # Нужно понять - надо ли оставлять properties, они нужны для выполнения команд создания БД, 
    # дополнительно к скрипту
    def establish_connection(self, properties: list[str] = [], dirpath: str = './') -> None:
        '''Устанавливает соединение c базой в path и, если БД отсутствует,
        то пересоздает ее на основе указанного скрипта.'''
        path = f"{dirpath}{self.__name}"
        if not os.path.isfile(path):
            self._createdatabase_(path)
        else:
            self._connection_ = sqlite.connect(path)

    def _createdatabase_(self, path: str) -> None:
        '''Создает базу данных на основе скрипта.'''
        self._connection_ = sqlite.connect(path)
        cursor = self._connection_.cursor()
        # Создаем таблицы
        cursor.execute('''
            CREATE TABLE logs (
                id integer NOT NULL AUTOINCREMENT,
                message TEXT, 
                time TEXT
            );
        ''')        
        # for property in properties:
        #     cursor.execute(statsment)
        self._connection_.commit()

    def execute(self, command: str, *params): 
        cursor = self._connection_.cursor()
        result = cursor.execute(command, params)
        self._connection_.commit()
        return result
    
    def addlog(self, messages: list[str]):
        cursor = self._connection_.cursor()
        sql = "INSERT INTO projects(message, time) VALUES(?,?)"
        time = datetime.datetime.now().isoformat()
        return cursor.execute(sql, list(product(messages, [time])))
    
    def closeconnection(self) -> None:
        '''Закрывает соединение с базой.'''
        self._connection_.close()