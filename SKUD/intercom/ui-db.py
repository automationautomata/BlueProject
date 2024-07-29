import json
from typing import Callable

from SKUD.ORM.database import DatabaseConnection
from SKUD.ORM.loggers import Logger
from SKUD.ORM.queries.templates import query_for_table


class DbAnswer:
    def __init__(self, answer_type: str, data: list[tuple], error: str) -> None:
        self.answer_type = answer_type
        self.data = convert(data)
        self.error = error
        
def convert(data: list[tuple]) -> list[list]:
    return [list(row) for row in data]

class UiController:
    def __init__(self, skud_db: DatabaseConnection, logger: Logger = None) -> None:
        self.skud_db = skud_db
        self.skud_db.establish_connection()
        self.logger = logger

    def action_query_map(self) -> dict[str, Callable]:
        actions = {"entity query": self.entity_query, 
                   "accesscontrol query": self.accesscontrol_query}
        return actions

    def entity_query(self, data: str) -> tuple[str, str]:
        return self.__tablequery__("entities_view", data)
        
    def accesscontrol_query(self, data: str) -> tuple[str, str]:
        return self.__tablequery__("access_rules_view", data)
            
    def __tablequery__(self, table: str, data: str) -> tuple[str, str]: 
        try: 
            params = json.load(data)
            col_names = list(map(lambda row: row[0], 
                                self.skud_db.execute(f"SELECT c.name FROM pragma_table_info('{table}') c;")))
            interval = (params["start"], 100 + params["start"])

            sql = query_for_table(table, col_names, interval, 
                            params["order_column"], params["order_type"])
            res = convert(self.skud_db.execute(sql))
            return '{'+f"\"rows\": \"{res}\""+'}', ""
        except NameError:
            if self.logger:
                self.logger.addlog(f"In UiController.__tablequery__ with table = {table} and data = {data} ERROR: {NameError}")
            return "{\"rows\": \"[]\"}", str(NameError)
