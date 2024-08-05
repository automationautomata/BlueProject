import copy
import json

from ORM.database import DatabaseConnection
from ORM.entities.tables import VisitsHistory
from ORM.loggers import VisitLogger, Logger
from hardware.tools import ardions_configuring

class AccessController:
    '''Класс для управления несолькими ардуино и взаимодействия с БД'''
    def __init__(self, skud: DatabaseConnection, ports: list[str], visits_db: VisitLogger, logger: Logger = None) -> None:
        '''`skud` - класс для соединения с БД скуда, `ports` - список портов, к которым подключены устройства, 
        `visits_db` - класс для соединения с БД инофрмации, полученной от устройств, 
        `logger` - класс для сохранения ошибок и дополнительной информации'''
        self.skud = skud
        self.skud.establish_connection()
        self.visits_db = visits_db
        handler_kwargs = {"visits_db": copy.deepcopy(self.visits_db), "logger": logger}
        self.visits_db.establish_connection()

        self.arduinos_therad, self.arduinos = ardions_configuring(ports, self.arduino_handler, handler_kwargs)
        self.logger = logger

    def arduino_handler(self, port: str, data: bytes, **kwargs) -> None:
        '''Обработчик приходящих с ардуино сообщений, `port` - порт, к которому подключено устройство, 
        `data` - полученные данные'''
        try: 
            print("arduino_handler", data)
            msg = json.loads(data.decode('utf-8'))
            if msg["type"] == "pass":
                kwargs["visits_db"].establish_connection()
                if "key" in msg.keys():
                    b = kwargs["visits_db"].addvisit(VisitsHistory(port, msg["key"]))
                    print(b)
        except NameError:
            if kwargs["logger"]:
                kwargs["logger"].addlog(f"In AccessController.arduino_handler() with port = {port} and data = {data} ERROR: {NameError}")
            print(NameError)

    def distribute_keys(self, room_port: dict[int, str]) -> None:
        '''Распределяет ключи по устройствам. `room_port` - словарь, где ключ - комната, а занчение - название порта'''
        sql = f'''SELECT entities.card, access_rules.room from entities INNER JOIN access_rules 
                                        ON entities.right = access_rules.right
                                                    WHERE entities.date_time_end IS NULL 
                                                        AND access_rules.date_time_end IS NULL;'''
        cards = self.skud.execute_query(sql)
        #print("distribute_keys", cards)
        for room, port in room_port.items():
            msg = list(map(lambda row: row[0], filter(lambda row: row[1] == room, cards)))
            self.arduinos[port].write('{'+f"\"cards\": \"{msg}\""+'}')

    def start(self, room_port: dict[int, str]) -> None:
        '''Запустить поток обработки событий с ардуино'''
        # for ard in self.arduinos.values():
        #     ard.open()
        self.arduinos_therad.start()
        self.distribute_keys(room_port)
