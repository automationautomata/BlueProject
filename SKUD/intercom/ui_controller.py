import json
from typing import Callable

from ORM.database import DatabaseConnection
from ORM.queries.templates import query_for_table
from remote.tools import Answer

from intercom.auth_controller import Tokens


class UiController:
    def __init__(self, skud_db: DatabaseConnection, logger: DatabaseConnection = None) -> None:
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
        
    def verify(self, **kwargs) -> bool:
        try:
            return self.tokens.check_token(int(kwargs["token"]), int(kwargs["id"]))
        except BaseException as error:
            if self.logger:
                self.logger.addlog(f"In UiController.verify with data = {kwargs} ERROR: {error}")
            return Answer([], str(error))


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
    

