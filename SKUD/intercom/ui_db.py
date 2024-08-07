from abc import ABC
import json
import random as rnd
from typing import Any, Callable

from ORM.database import DatabaseConnection
from ORM.loggers import Logger, VisitLogger
from ORM.queries.templates import condition_query, query_for_table
from general.singleton import Singleton
from remote.tools import Actions
from remote.ui import Answer

class Tokens(Singleton):
    '''Класс для хранения токенов сессий'''
    def __init__(self) -> None:
        self.__randmax = 2**32
        self.__tokens = {}

    def istoken(self, token: int) -> bool:
        '''Проверяет есть ли токен'''
        return token in self.__tokens
            
    def add(self, id: str | int) -> int:
        '''Генерирует новый токен с `id`'''
        token = rnd.randint(0, self.__randmax)
        self.__tokens[token] = id
        return token
    
    def remove(self, id: str | int) -> bool:
        '''Удаление токена'''
        if self.__tokens:
            return True
        return False
        
class AuthenticationController:
    def __init__(self, remote_right: int, visits_db: VisitLogger, skud_db: DatabaseConnection, Debug: bool = False) -> None:
        self.visits_db = visits_db
        self.visits_db.establish_connection()
        self.skud_db = skud_db
        self.skud_db.establish_connection()
        self.remote_rule = remote_right

        sql = condition_query("access_rules", ["room"], f"right = {remote_right}")
        self.remote_rooms = {row[0] for row in self.skud_db.execute_query(sql)}
        self.tokens = Tokens()

        self.Debug = Debug
    
    def verificator(self, data) -> Answer:  
        try:
            msg = json.loads(data)
            if msg['id'] in self.remote_rooms:
                sql = condition_query("entities", ["card"], 
                                     f"right = {self.remote_right} and card = {msg['key']}")
                card = self.skud_db.execute_query(sql) 

                #### DEBUG ####
                if self.Debug: print("data:", data, "card:", card)

                if len(card) == 1:
                    token = self.tokens.add(msg['id'])
                    return Answer(token, "")
                return Answer(0, "Invalid card")
            return Answer(0, "Invalid room")
        except NameError:
            
            #### DEBUG ####
            if self.Debug: print("ERROR:", str(NameError))

            return Answer(0, str(NameError))
        
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
        except NameError:
            if self.logger:
                self.logger.addlog(f"In UiController.__tablequery__ with table = {table} and data = {data} ERROR: {NameError}")
            return Answer([], str(NameError))
        
    def verify(self, data: Any) -> bool:
        try:
            msg = json.loads(data)
            return self.tokens.istoken(msg["token"])
        except NameError:
            if self.logger:
                self.logger.addlog(f"In UiController.verify with data = {data} ERROR: {NameError}")
            return Answer([], str(NameError))

class UiSKUDController(UiController):
    '''Класс для обработки запросов к БД СКУДа'''
    def action_query_map(self) -> dict[str, Callable]:
        actions = {"entities query"   : self.entity_query, 
                   "accessrules query": self.accessrules_query}
        return actions

    def entity_query(self, data: str) -> Answer:
        return self.__tablequery__("entities_view", data)
        
    def accessrules_query(self, data: str) -> Answer:
        return self.__tablequery__("access_rules_view", data)

class UiVisitsController(UiController):
    '''Класс для обработки запросов к БД посещений'''
    def action_query_map(self) -> dict[str, Callable]:
        actions = {"visits query"         : self.visits_query, 
                   "remote_sessions query": self.remote_sessions_query}
        return actions

    def visits_query(self, data: str) -> Answer:
        return self.__tablequery__("visits_history", data)
        
    def remote_sessions_query(self, data: str) -> Answer:
        return self.__tablequery__("remote_sessions", data)
    

