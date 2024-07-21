
from ORM.database import AccessControl
import SKUD.config as config

def getentites(data: str) -> str:
    db = AccessControl(config.SCRIPT_PATH, config.DB_NAME)
    db.establish_connection(config.ROOT_DIR)
    condition = " and ".join(f"{data["column"]} = {user}" for user in data["users"])
    join_query = f"(select * from entities where {condition}) as e"
    if data["extra"] == "rights":
        join_query += " inner join rights on e.right = rights.right"
    elif data["extra"] == "cards":   
        join_query += " inner join cards on cards.id = e.card"
    elif data["extra"] == "both":
        join_query = f"(({join_query} inner join rights on e.right = rights.right) as er 
                                        inner join cards on cards.id = er.card)"
    result = db.execute(f'''select * from {join_query}''')
    print(result)
    return result

def createquery(main_table: str, join_tables: list[(str, str, str)] = None, 
                conditions: list[str] = None):
    pass
def getaccessrules(rights):
    db = AccessControl(config.SCRIPT_PATH, config.DB_NAME)
    db.establish_connection(config.ROOT_DIR)
    condition = " and ".join(f"sid = {right}" for right in rights)
    db.execute(f'''select * from (((select * from access_rules where {condition}) as e 
                                    inner join rights on e.right = rights.right) as er 
                                        inner join cards on cards.id = er.card)''')

def convert(data: list[tuple]):


