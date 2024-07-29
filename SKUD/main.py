import os
import sys
import time
sys.path.append(os.getcwd())

from ORM.database import DatabaseConnection
from ORM.loggers import VisitLogger
from config import ARDUINO_PORTS, ROOM_PORT_MAP
from intercom.arduino_db import AccessController

skud_db = DatabaseConnection(scriptpath=".\\dbscripts\\skud_script.sql",
                             name="SKUD", dirpath=".\\DB\\")
visits_db = VisitLogger(name="visits_db", dirpath=".\\DB\\")

ac = AccessController(skud=skud_db, ports=ARDUINO_PORTS,
                      visits_db=visits_db)

ac.start(ROOM_PORT_MAP)
time.sleep(2)
print(visits_db.execute_query("SELECT * FROM history;"))