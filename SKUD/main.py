import os
import sys
import time

from intercom.ui_db import UiController
from remote.ui import create_tornado_server
sys.path.append(os.getcwd())

from ORM.database import DatabaseConnection
from ORM.loggers import VisitLogger
from config import ARDUINO_PORTS, ROOM_PORT_MAP, URL
from intercom.arduino_db import AccessController

# Запуск и нстройка работы ардуино
skud_db = DatabaseConnection(scriptpath=".\\dbscripts\\skud_script.sql",
                             name="SKUD", dirpath=".\\DB\\")
visits_db = VisitLogger(name="visits_db", dirpath=".\\DB\\")

ac = AccessController(skud=skud_db, ports=ARDUINO_PORTS,
                      visits_db=visits_db)

# Запуск и нстройка работы сервера
ac.start(ROOM_PORT_MAP)
time.sleep(2)
print(visits_db.execute_query("SELECT * FROM visits_history;"))

skud_db = DatabaseConnection(scriptpath=".\\dbscripts\\skud_script.sql",
                             name="SKUD", dirpath=".\\DB\\")
ui = UiController(skud_db=skud_db)
create_tornado_server(actions=ui.action_query_map(), port=URL[1])
time.sleep(2)