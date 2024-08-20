import json
from typing import Callable, Dict

from ORM.database import DatabaseConnection
from ORM.loggers import Logger
from ORM.templates import condition_query, sort_query, \
                          insert, update
from remote.tools import Answer

from auth_controller import Tokens


class UiController:
    def __init__(self, skud_db: DatabaseConnection, logger: Logger = None) -> None:
        '''`skud_db` - соединение с БД СКУДа, `logger` - логгер'''
        self.skud_db = skud_db
        self.skud_db.establish_connection()
        self.logger = logger
        if self.logger:
            self.logger.establish_connection()
        self.tokens = Tokens()

    def __table_query__(self, table: str, data: str) -> Answer:
        '''Запрос к таблице `table`, `data` - параметры запроса. возвращает ответ Answer, где data - спиоск'''
        try: 
            params = sort_query(json.loads(data))
            col_names = self.skud_db.table_cols(table)
            interval = (params["start"], 100 + params["start"])
            if params["null_col"] != "":
                table = condition_query(table, col_names, f"{params["null_col"]} IS NOT NULL")

            sql = sort_query(table, col_names, interval, 
                            params["order_column"], params["order_type"])
            
            res = self.skud_db.execute_query(sql)
            return Answer(self.skud_db.rows_to_dicts(col_names, res), "")
        except BaseException as error:
            if self.logger:
                self.logger.addlog(f"In UiController.__table_query__ with table = {table} and data = {data} ERROR: {error}")
            return Answer([], str(error))
    
    def __table_insert__(self, table: str, data: str) -> Answer:
        '''Запрос к таблице `table`, `data` - параметры запроса. возвращает ответ Answer, где data - спиоск'''
        try: 
            inserted: dict = json.loads(data)
            col_names = []
            vals = []
            for key, val in inserted:
                col_names.append(key)
                vals.append(val)
            sql = insert(table, col_names)
            res = self.skud_db.execute_query(sql, *vals)
            print(res)
            return Answer("", "")
        except BaseException as error:
            if self.logger:
                self.logger.addlog(f"In UiController.__table_query__ with table = {table} and data = {data} ERROR: {error}")
            return Answer([], str(error))

    def __table_update__(self, table: str, data: str) -> Answer:
        '''Запрос к таблице `table`, `data` - параметры запроса. возвращает ответ Answer, где data - спиоск'''
        try: 
            updated: dict = json.loads(data)
            col_names = []
            vals = []
            for key, val in updated["values"]:
                col_names.append(key)
                vals.append(val)
            pk = self.skud_db.table_pk("table")
            sql = update(table, col_names, f"{pk} = {updated["key"]}")
            res = self.skud_db.execute_query(sql)
            print(res)  
            return Answer("", "")
        except BaseException as error:
            if self.logger:
                self.logger.addlog(f"In UiController.__table_query__ with table = {table} and data = {data} ERROR: {error}")
            return Answer([], str(error))

    def verify(self, **kwargs) -> bool:
        '''Проверяет '''
        try:
            return self.tokens.check_token(int(kwargs["token"]), int(kwargs["id"]))
        except BaseException as error:
            if self.logger:
                self.logger.addlog(f"In UiController.verify with data = {kwargs} ERROR: {error}")
            return Answer([], str(error))

class UiSKUDController(UiController):
    '''Класс для обработки запросов к БД СКУДа'''
    def actions_map(self) -> dict[str, Callable]:
        '''Создает связку между запросом и функцией, ключ - ресурс'''
        actions = { "entities"   : { "get"  : self.entity_query, 
                                     "post" : self.entity_insert     }, 
                    "rights"     : { "get"  : self.rights_query,
                                     "post" : self.rooms_insert      },
                    "rooms"      : { "get"  : self.rooms_query, 
                                     "post" : self.rooms_insert      },
                    "cards"      : { "get"  : self.cards_query, 
                                     "post" : self.cards_insert      },
                    "accessrules": { "get"  : self.accessrules_query,
                                     "post" : self.accessrules_insert}}
        return actions
    
    def rights_query(self, data) -> Answer:
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

    def rooms_update(self, data) -> Answer:
        '''Для вставки - нужен словарь, где ключи - поля таблицы.'''
        return self.__table_insert__("room" ,data)


    def entity_insert(self, data) -> Answer:
        return self.__table_insert__("entities", data)

    def accessrules_insert(self, data) -> Answer:
        return self.__table_insert__("access_rules", data)

    def rooms_insert(self, data) -> Answer:
        '''Для вставки - нужен словарь, где ключи - поля таблицы.'''
        return self.__table_insert__("room" ,data)
    
    def rights_insert(self, data) -> Answer:
        '''Для вставки - нужен словарь, где ключи - поля таблицы.'''
        return self.__table_insert__("rights" ,data)
    
    def cards_insert(self, data) -> Answer:
        '''Для вставки - нужен словарь, где ключи - поля таблицы.'''
        return self.__table_insert__("cards" ,data)

    def entity_query(self, data: str) -> Answer:
        return self.__table_query__("entities_view", data)
        
    def accessrules_query(self, data: str) -> Answer:
        return self.__table_query__("access_rules_view", data)
        
    def rooms_query(self, data: str) -> Answer:
        return self.__table_query__("rooms", data)
        
    def cards_query(self, data: str) -> Answer:
        return self.__table_query__("cards", data)


class UiVisitsController(UiController):
    '''Класс для обработки запросов к БД посещений'''
    def actions_map(self) -> dict[str, Callable]:
        actions = {"visits query"         : self.visits_query, 
                   "remote_sessions query": self.remote_sessions_query}
        return actions

    def visits_query(self, data: str) -> Answer:
        return self.__table_query__("visits_history", data)
        
    def remote_sessions_query(self, data: str) -> Answer:
        return self.__table_query__("remote_sessions", data)
    

