import logging
import os
import time

from controllers.auth_controller import AuthenticationController
from controllers.access_controller import AccessController
from controllers.ui_controller import SkudQueryHandler, UiController

from remote.server import create_tornado_server
from ORM.database import DatabaseConnection
from ORM.loggers import VisitLogger
from general.config import (ARDUINO_PORTS, ROOM_PORT_MAP, URL, 
                            DB_DIR,
                            SKUD_SCRIPT_PATH, SKUD_DB_NAME, 
                            VISITS_SCRIPT_PATH, VISITS_DB_NAME)
print(os.getcwd(), "ddd")
logging.basicConfig(filename=f"{os.getcwd()}/py_log.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")


# Запуск и нстройка работы ардуино
skud_db = DatabaseConnection(name=SKUD_DB_NAME, dirpath=DB_DIR, 
                             scriptpath=SKUD_SCRIPT_PATH)

visits_db = VisitLogger(name=VISITS_DB_NAME, dirpath=DB_DIR, 
                        scriptpath=VISITS_SCRIPT_PATH)

ac = AccessController(skud=skud_db, ports=ARDUINO_PORTS,
                      visits_db=visits_db)

ac.start(ROOM_PORT_MAP)
time.sleep(2)
print('\n'.join(visits_db.execute_query("SELECT * FROM visits_history;")))

# Запуск и нстройка работы сервера

ui_controller = UiController(skud_db=skud_db)
auth_constroller = AuthenticationController(0, visits_db, skud_db)

router = [(r"\\ui", SkudQueryHandler, ui_controller)]
t, _ = create_tornado_server(URL[1], router, auth=auth_constroller.authenticatior)

t.start()
time.sleep(2)
##### Wiegand ######