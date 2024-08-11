import time

from controllers.access_controller import AccessController
from controllers.ui_controllers import UiSKUDController

from remote.ui import create_tornado_server
from ORM.database import DatabaseConnection
from ORM.loggers import VisitLogger
from general.config import (ARDUINO_PORTS, ROOM_PORT_MAP, URL, 
                            DB_DIR,
                            SKUD_SCRIPT_PATH, SKUD_DB_NAME, 
                            VISITS_SCRIPT_PATH, VISITS_DB_NAME)

# Запуск и нстройка работы ардуино
skud_db = DatabaseConnection(name=SKUD_DB_NAME, dirpath=DB_DIR, 
                             scriptpath=SKUD_SCRIPT_PATH)

visits_db = VisitLogger(name=VISITS_DB_NAME, dirpath=DB_DIR, 
                        scriptpath=VISITS_SCRIPT_PATH)

ac = AccessController(skud=skud_db, ports=ARDUINO_PORTS,
                      visits_db=visits_db)

# Запуск и нстройка работы сервера
ac.start(ROOM_PORT_MAP)
time.sleep(2)
print('\n'.join(visits_db.execute_query("SELECT * FROM visits_history;")))

skud_db = DatabaseConnection(name=SKUD_DB_NAME, dirpath=DB_DIR, 
                             scriptpath=SKUD_SCRIPT_PATH)

t, _ = create_tornado_server(port=URL[1])
t.start()
time.sleep(2)
##### Wiegand ######