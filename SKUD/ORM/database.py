from abc import ABC, abstractmethod
import sqlite3
import os
import threading

from general.singleton import Singleton

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

class DatabaseConnection(DatabaseABC, Singleton):
    def __init__(self, scriptpath: str, name: str, dirpath: str = ".\\") -> None:
        '''`scriptpath` - путь к скрипту, создающему бд,
        `name` - название БД, `dirpath` - папка с БД'''
        self.__scriptpath = scriptpath
        self.__name = name
        self.__dirpath = dirpath
        self._connection_ = {} #: dict[int, sqlite3.Connection] = {}
        
    def threadsafe_connect(self) -> sqlite3.Connection:
        path = f"{self.__dirpath}{self.__name}"
        thread_id = threading.get_native_id()
        if thread_id not in self._connection_.keys():
            self._connection_[thread_id] = sqlite3.connect(path)        
        return self._connection_[thread_id]

    def establish_connection(self) -> None:
        '''Устанавливает соединение c базой и, если БД отсутствует,
        то пересоздает ее на основе указанного скрипта.'''
        path = f"{self.__dirpath}{self.__name}"
        if not os.path.exists(path):
            self._createdatabase_()
        else: 
            try: 
                self.threadsafe_connect().cursor()
            except: 
                thread_id = threading.get_native_id()
                self._connection_[thread_id] = sqlite3.connect(path)

    def _createdatabase_(self) -> None:
        '''Создает базу данных на основе скрипта.'''
        conn = self.threadsafe_connect()
        cursor = conn.cursor()

        with open(self.__scriptpath, mode="r+", encoding="utf8") as scriptfile:
            script = scriptfile.read()
            cursor.executescript(script)
            conn.commit()

    def execute_query(self, command: str, *params) -> list[tuple]: 
        '''Выполняет указанную команду command с параметрами params (см. документацию SQLite).'''
        conn = self.threadsafe_connect()
        cursor = conn.cursor()
        result = cursor.execute(command, params).fetchall()
        conn.commit()
        return result
    
    def execute(self, command: str, *params) -> list[tuple]: 
        '''Выполняет указанную команду command с параметрами params (см. документацию SQLite).'''
        conn = self.threadsafe_connect()
        cursor = conn.cursor()
        result = cursor.execute(command, params)
        conn.commit()
        return result
        
    def table_cols(self, table: str):
        sql = f"SELECT c.name FROM pragma_table_info('{table}') as c;"
        return list(map(lambda row: row[0], self.execute_query(sql)))
    
    def rows_to_dicts(self, col_names: list[str], rows: list[tuple]) -> list[dict]:
        data = []
        for row in rows:
            dict_row = {col: val for val, col in zip(row, col_names)}
            data += dict_row
        return data

    def close(self) -> None:
        '''Закрывает соединение с БД'''
        for key in self._connection_.keys():
            self._connection_[key].close()
            del self._connection_[key]
    