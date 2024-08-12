import json
from typing import Callable

from ORM.database import DatabaseConnection
from ORM.loggers import Logger
from ORM.templates import insert, query_for_table
from remote.tools import Answer

from .auth_controller import Tokens


class UiController:
    def __init__(self, skud_db: DatabaseConnection, logger: Logger = None) -> None:
        '''`skud_db` - соединение с БД СКУДа, `logger` - логгер'''
        self.skud_db = skud_db
        self.skud_db.establish_connection()
        self.logger = logger
        if self.logger:
            self.logger.establish_connection()
        self.tokens = Tokens()

    def __tablequery__(self, table: str, data: str) -> Answer:
        '''Запрос к таблице `table`, `data` - параметры запроса. возвращает ответ Answer, где data - спиоск'''
        try: 
            params = json.loads(data)
            col_names = self.skud_db.table_cols(table)
            interval = (params["start"], 100 + params["start"])

            sql = query_for_table(table, col_names, interval, 
                            params["order_column"], params["order_type"])

            res = self.skud_db.execute_query(sql)
            return Answer(self.skud_db.rows_to_dicts(col_names, res), "")
        except BaseException as error:
            if self.logger:
                self.logger.addlog(f"In UiController.__tablequery__ with table = {table} and data = {data} ERROR: {error}")
            return Answer([], str(error))
    
    def __table_insert__(self, table: str, inserted: dict) -> Answer:
        '''Запрос к таблице `table`, `data` - параметры запроса. возвращает ответ Answer, где data - спиоск'''
        try: 
            sql = insert(table, inserted.keys())
            res = self.skud_db.execute_query(sql)
            print(res)
            return Answer("", "")
        except BaseException as error:
            if self.logger:
                self.logger.addlog(f"In UiController.__tablequery__ with table = {table} and data = {data} ERROR: {error}")
            return Answer([], str(error))
        
    def verify(self, **kwargs) -> bool:
        try:
            return self.tokens.check_token(int(kwargs["token"]), int(kwargs["id"]))
        except BaseException as error:
            if self.logger:
                self.logger.addlog(f"In UiController.verify with data = {kwargs} ERROR: {error}")
            return Answer([], str(error))

class UiSKUDController(UiController):
    '''Класс для обработки запросов к БД СКУДа'''
    def actions_map(self) -> dict[str, Callable]:
        actions = {"entities"   : { "get"  : self.entity_query, 
                                    "post" : self.entity_insert }, 
                   "rights"     : { "get"  : self.rights_query  },
                   "accessrules": { "get"  : self.accessrules_query}}
        return actions
    
    def rights_query(self, data):
        try:
            msg = json.loads(data)
            sql = "SELECT id, name FROM rights"
            if  not msg['all']:
                sql += "WHERE date_time_end IS NULL"
            print(";;;")

            res = self.skud_db.execute_query(sql)
            print("res", res)

            data = self.skud_db.rows_to_dicts(["id", "name"], res)
            print(data)
            return Answer(data, "")
        except BaseException as error:
            return Answer("", str(error))

    def entity_insert(self, data):
        try: 
            msg = json.loads(data)
            return self.__table_insert__("entities", msg)
        except BaseException as error:
            return Answer("", error)
    
    def entity_query(self, data: str) -> Answer:
        return self.__tablequery__("entities_view", data)
        
    def accessrules_query(self, data: str) -> Answer:
        return self.__tablequery__("access_rules_view", data)


class UiVisitsController(UiController):
    '''Класс для обработки запросов к БД посещений'''
    def actions_map(self) -> dict[str, Callable]:
        actions = {"visits query"         : self.visits_query, 
                   "remote_sessions query": self.remote_sessions_query}
        return actions

    def visits_query(self, data: str) -> Answer:
        return self.__tablequery__("visits_history", data)
        
    def remote_sessions_query(self, data: str) -> Answer:
        return self.__tablequery__("remote_sessions", data)
    

