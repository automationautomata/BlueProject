import os.path
from abc import ABC, abstractmethod
import sqlite3 as sqllite

# Шаблон класса, который настраивает базу данных
class DatabaseProperties(ABC):
    @abstractmethod
    def useproperties(self, cursor: sqllite.Cursor) -> None: 
        pass
# Шаблон класса для установки соединений с БД
class DatabaseConnection(ABC):
    @abstractmethod
    def establish_connection(self, rootpath: str) -> None:
        pass
    @abstractmethod
    def establish_connection(self, properties: list[DatabaseProperties], 
                            rootpath: str, name: str) -> None:
        pass
    # Метод для создания базы или, при ее утрате, восстановления
    @abstractmethod
    def _createdatabase_(self) -> None: 
        pass
    @abstractmethod
    def execute(self, command: str, *params) -> None: 
        pass
    @abstractmethod
    def closeconnection(self) -> None: 
        pass


class AccessControl(DatabaseConnection):
    _instance = None
    def __new__(cls, name):
        if not cls._instance:
            cls._instance = object.__new__(cls)
            cls.__name__ = name
        return cls._instance
    
    def establish_connection(self, rootpath = './') -> None:
        self.__rootpath__ = rootpath
        if not os.path.isfile(f"{rootpath}{self.__name__}"):
            self.__createdatabase__()
    
    def establish_connection(self, properties: list[DatabaseProperties], rootpath = './') -> None:
        self.__rootpath__ = rootpath
        self.__properties__ = properties
        #self.__name__ = name
        if not os.path.isfile(f"{rootpath}{self.__name__}"):
            self.__createdatabase__()
        else:
            self._connection_ = sqllite.connect(f"{self.__rootpath__}{self.__name__}")
    
    def _createdatabase_(self):
        self._connection_ = sqllite.connect(f"{self.__rootpath__}{self.__name__}")
        cursor = self._connection_.cursor()

        # Создаем таблицы
        cursor.execute('''
            CREATE TABLE cards (
                card VARCHAR(4) PRIMARY KEY,
                status VARCHAR(1) NOT NULL
            );
            CREATE TABLE rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(40) NOT NULL
            );
            CREATE TABLE rights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                right INTEGER NOT NULL,
                FOREIGN KEY (room) REFERENCES rooms (id)
                UNIQUE(right, room)
            );
            CREATE TABLE entities (
                FOREIGN KEY (card) REFERENCES cards (card),
                sid INTEGER PRIMARY KEY,
                type VARCHAR(1) NOT NULL,
                FOREIGN KEY (right) REFERENCES rights (id)
            );
        ''')
        for property in self.__properties__:
            property.useproperties(cursor)
        self._connection_.commit()

    def execute(self, command, *params): 
        cursor = self._connection_.cursor()
        return cursor.execute(command, params)
    
    def closeconnection(self):
        self._connection_.close()

