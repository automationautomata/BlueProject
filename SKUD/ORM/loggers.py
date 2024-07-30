from ORM.database import DatabaseConnection
from ORM.entities.tables import VisitsHistory
from datetime import datetime

class Logger(DatabaseConnection):
    __scriptpath = ".\\dbscripts\\logger_script.sql"
    def __init__(self, name: str, dirpath: str = "./") -> None:
        super().__init__(Logger.__scriptpath, name, dirpath)
    
    def addlog(self, messages: list[str]):
        cursor = self._connection_.cursor()
        sql = "INSERT INTO projects(message, time) VALUES(?,?)"
        time = datetime.now().isoformat()
        fmt = lambda msg: (msg, time)
        try:
            cursor.execute(sql, list(map(fmt, messages)))
            self._connection_.commit()
            return True
        except: 
            return False

class VisitLogger(DatabaseConnection):
    __scriptpath = ".\\dbscripts\\visits_script.sql"
    def __init__(self, name: str, dirpath: str = "./") -> None:
        super().__init__(VisitLogger.__scriptpath, name, dirpath)

    def addrow(self, message: VisitsHistory):
        cursor = self._connection_.cursor()
        sql = "INSERT INTO visits_history (port, message, pass_time) VALUES (?,?,?);"
        data = (message.port, message.message, message.pass_time)
        try: 
            cursor.execute(sql, data)
            self._connection_.commit()
            return True
        except NameError: 
            print("ERR", NameError)
            return False
    

    