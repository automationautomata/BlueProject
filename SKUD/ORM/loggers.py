from ORM.database import DatabaseConnection
from ORM.entities.tables import VisitsHistory
from datetime import datetime

class Logger(DatabaseConnection):
    '''Класс для установки соединения с БД логгером'''
    __scriptpath = ".\\dbscripts\\logger_script.sql"
    
    def __init__(self, name: str, dirpath: str = "./") -> None:
        '''`name` - название БД, `dirpath` - путь к БД.'''
        super().__init__(Logger.__scriptpath, name, dirpath)
    
    def addlog(self, row: list[str]):
        '''Добавляет запись в таблицу истории посещений комнат. `row` - добавляемая строка'''
        cursor = self._connection_.cursor()
        sql = "INSERT INTO projects(message, time) VALUES(?,?)"
        time = datetime.now().isoformat()
        fmt = lambda msg: (msg, time)
        try:
            cursor.execute(sql, list(map(fmt, row)))
            self._connection_.commit()
            return True
        except: 
            return False

class VisitLogger(DatabaseConnection):
    '''Класс для установки соединения с БД посещений'''
    __scriptpath = ".\\dbscripts\\visits_script.sql"

    def __init__(self, name: str, dirpath: str = "./") -> None:
        '''`name` - название БД, `dirpath` - путь к БД.'''
        super().__init__(VisitLogger.__scriptpath, name, dirpath)

    def addvisit(self, row: VisitsHistory):
        '''Добавляет запись в таблицу истории посещений комнат. `row` - добавляемая строка'''
        cursor = self._connection_.cursor()
        sql = "INSERT INTO visits_history (port, message, pass_time) VALUES (?,?,?);"
        data = (row.port, row.message, row.pass_time)
        try: 
            cursor.execute(sql, data)
            self._connection_.commit()
            return True
        except NameError: 
            print("ERR", NameError)
            return False
    

    