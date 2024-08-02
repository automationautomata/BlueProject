from abc import ABC, abstractmethod
import sqlite3
import os

# Шаблон класса для установки соединений с БД
class DatabaseABC(ABC):
    @abstractmethod
    def establish_connection(self, rootpath: str) -> None:
        pass
    @abstractmethod
    def establish_connection(self, properties: list[str] = [], dirpath: str = './') -> None:
        pass
    # Метод для создания базы или, при ее утрате, восстановления
    @abstractmethod
    def _createdatabase_(self, path: str) -> None: 
        pass
    @abstractmethod
    def execute_query(self, command: str, *params) -> None: 
        pass
    @abstractmethod
    def close(self) -> None: 
        pass


class DatabaseConnection(DatabaseABC):
    def __init__(self, scriptpath: str, name: str, dirpath: str = "./") -> None:
        '''`scriptpath` - путь к скрипту, создающему бд,
        `name` - название БД, `dirpath` - папка с БД'''
        self.__scriptpath = scriptpath
        self.__name = name
        self.__dirpath = dirpath
        self._connection_ = None

    def establish_connection(self) -> None:
        '''Устанавливает соединение c базой и, если БД отсутствует,
        то пересоздает ее на основе указанного скрипта.'''
        path = f"{self.__dirpath}{self.__name}"
        if not os.path.exists(path):
            self._createdatabase_(path)
        elif not self._connection_: 
            self._connection_ = sqlite3.connect(path)
        else: 
            try: 
                self._connection_.cursor()
            except: 
                self._connection_ = sqlite3.connect(path)

    def _createdatabase_(self, path: str) -> None:
        '''Создает базу данных на основе скрипта.'''
        self._connection_ = sqlite3.connect(path)
        cursor = self._connection_.cursor()

        with open(self.__scriptpath, "r+") as scriptfile:
            script = scriptfile.read()
            cursor.executescript(script)
            self._connection_.commit()

    def execute_query(self, command: str, *params) -> list[tuple]: 
        '''Выполняет указанную команду command с параметрами params (см. документацию SQLite).'''
        cursor = self._connection_.cursor()
        result = cursor.execute(command, params).fetchall()
        self._connection_.commit()
        return result
    
    def execute(self, command: str, *params) -> list[tuple]: 
        '''Выполняет указанную команду command с параметрами params (см. документацию SQLite).'''
        cursor = self._connection_.cursor()
        result = cursor.execute(command, params)
        self._connection_.commit()

    def close(self) -> None:
        '''Закрывает соединение с БД'''
        self._connection_.close()