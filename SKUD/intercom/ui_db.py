from abc import ABC
import json
from typing import Any, Callable

from ORM.database import DatabaseConnection
from ORM.loggers import Logger
from ORM.queries.templates import query_for_table
from remote.tools import Actions
from remote.ui import Answer

class UiSkudController(Actions):
    def __init__(self, skud_db: DatabaseConnection, logger: Logger = None) -> None:
        self.skud_db = skud_db
        self.skud_db.establish_connection()
        self.logger = logger

    def action_query_map(self) -> dict[str, Callable]:
        actions = {"entities query": self.entity_query, 
                   "accessrules query": self.accessrules_query}
        return actions

    def entity_query(self, data: str) -> tuple[str, str]:
        return self.__tablequery__("entities_view", data)
        
    def accessrules_query(self, data: str) -> tuple[str, str]:
        return self.__tablequery__("access_rules_view", data)
    
    def rows_to_dicts(self, col_names: list[str], rows: list[Any]) -> list[dict[str, Any]]:
        data = []
        for row in rows:
            elem = {}
            for val, col in zip(row, col_names):
                elem[col] = val
            data.append(elem)
        return data

    def __tablequery__(self, table: str, data: str) -> Answer: 
        try: 
            params = json.loads(data)
            col_names = list(map(lambda row: row[0], 
                                self.skud_db.execute_query(f"SELECT c.name FROM pragma_table_info('{table}') as c;")))
            interval = (params["start"], 100 + params["start"])

            sql = query_for_table(table, col_names, interval, 
                            params["order_column"], params["order_type"])
            #res = convert(self.skud_db.execute(sql))
            #return '{'+f"\"rows\": \"{res}\""+'}', ""
            res = self.skud_db.execute_query(sql)
            return Answer(self.rows_to_dicts(col_names, res), "")
        except NameError:
            if self.logger:
                self.logger.addlog(f"In UiController.__tablequery__ with table = {table} and data = {data} ERROR: {NameError}")
            return Answer([], str(NameError))

class UiVisitsController(Actions):
    def action_query_map(self) -> dict[str, Callable]:
        actions = {"entities query": self.entity_query, 
                   "accessrules query": self.accessrules_query}
        return actions