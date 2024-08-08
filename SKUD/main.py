import os
import sys
import time

from intercom.ui_controller import UiSKUDController
from remote.setting import create_tornado_server
sys.path.append(os.getcwd())

from ORM.database import DatabaseConnection
from ORM.loggers import VisitLogger
from general.config import ARDUINO_PORTS, ROOM_PORT_MAP, URL, \
                   SKUD_SCRIPT_PATH, DB_NAME, DB_DIR
from intercom.access_controller import AccessController

# Запуск и нстройка работы ардуино
skud_db = DatabaseConnection(scriptpath=SKUD_SCRIPT_PATH,
                             name=DB_NAME, dirpath=DB_DIR)
visits_db = VisitLogger(name="visits_db", dirpath=DB_DIR)

ac = AccessController(skud=skud_db, ports=ARDUINO_PORTS,
                      visits_db=visits_db)

# Запуск и нстройка работы сервера
ac.start(ROOM_PORT_MAP)
time.sleep(2)
print('\n'.join(visits_db.execute_query("SELECT * FROM visits_history;")))

skud_db = DatabaseConnection(scriptpath="SKUD_SCRIPT_PATH",
                             name=DB_NAME, dirpath=DB_DIR)
uiSkud = create_tornado_server(skud_db=skud_db)
t, _ = create_tornado_server(skud_actions=uiSkud, port=URL[1])
t.start()
time.sleep(2)