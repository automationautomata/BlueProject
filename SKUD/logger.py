import sqlite3 as sqlite
from database import DatabaseConnection, DatabaseProperties
from os import path
import datetime
from itertools import product
class Logger(DatabaseConnection):
    _instance = None
    def __new__(cls, name):
        if not cls._instance:
            cls._instance = object.__new__(cls)
            cls.__name__ = name
        return cls._instance
    
    def establish_connection(self, rootpath = './') -> None:
        self.__rootpath__ = rootpath
        if not path.isfile(f"{rootpath}{self.__name__}"):
            self.__createdatabase__()
    
    def establish_connection(self, properties: list[DatabaseProperties], rootpath = './') -> None:
        self.__rootpath__ = rootpath
        self.__properties__ = properties
        #self.__name__ = name
        if not path.isfile(f"{rootpath}{self.__name__}"):
            self.__createdatabase__()
        else:
            self._connection_ = sqlite.connect(f"{self.__rootpath__}{self.__name__}")
    
    def _createdatabase_(self):
        self._connection_ = sqlite.connect(f"{self.__rootpath__}{self.__name__}")
        cursor = self._connection_.cursor()

        cursor.execute('''
            CREATE TABLE logs (
                id integer NOT NULL AUTOINCREMENT,
                message VARCHAR(255), 
                time TEXT
            );
        ''')
        for property in self.__properties__:
            property.useproperties(cursor)
        self._connection_.commit()

    def execute(self, command, *params): 
        cursor = self._connection_.cursor()
        result = cursor.execute(command, params)
        self._connection_.commit()
        return result
    
    def addlog(self, messages):
        cursor = self._connection_.cursor()
        sql = "INSERT INTO projects(message, time) VALUES(?,?)"
        time = datetime.datetime.now().isoformat()
        return cursor.execute(sql, list(product(messages, [time])))
    
    def closeconnection(self):
        self._connection_.close()