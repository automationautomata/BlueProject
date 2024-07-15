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

class AccessControl():
    def __init__(self, scriptpath: str, name: str) -> None:
        '''scriptpath - путь к скрипту, создающему бд,
        name - название БД.'''
        self.__scriptpath = scriptpath
        self.__name = name

    def establish_connection(self, path: str = './') -> None:
        '''Устанавливает соединение и, если БД отсутствует,
        то пересоздает ее на основе указанного скрипта.'''
        #self.__path = path
        if not os.path.isfile(path):
            self._createdatabase_(path)
    
    # def establish_connection(self, properties: list[DatabaseProperties], path: str = './') -> None:
    #     '''Устанавливает соединение c базой в path и, если БД отсутствует,
    #     то пересоздает ее на основе указанного скрипта.'''
    #     #self.__path = path
    #     self.__properties__ = properties
    #     if not os.path.isfile(path):
    #         self._createdatabase_(path)
    #     else:
    #         self._connection_ = sqllite.connect(path)

    def __readscript__(self) -> str:
        '''Читает скрипт покомандно, используя ';' как разделитель.'''
        script = open(self.__scriptpath, "r+")
        sql = script.read().split(";")
        script.close() 
        return sql

    def _createdatabase_(self, path: str) -> None:
        '''Создает базу данных на основе скрипта.'''
        self._connection_ = sqllite.connect(path)
        cursor = self._connection_.cursor()
        statsments = self.__readscript__()
        # Создаем таблицы
        for statsment in statsments:
            cursor.execute(statsment)
        self._connection_.commit()

    def execute(self, command: str, *params) -> None: 
        '''Выполняет указанную команду command с параметрами params (см. документацию SQLite).'''
        cursor = self._connection_.cursor()
        result = cursor.execute(command, params)
        self._connection_.commit()
        return result
    
    def closeconnection(self) -> None:
        '''Закрывает соединение с базой.'''
        self._connection_.close()