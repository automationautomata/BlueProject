# Глобальные константы для СКУДа

import os

ROOT_DIR = os.getcwd() 
'''Корневая папка'''

DB_DIR = f"{ROOT_DIR}\\DB"
'''Путь к папке с БД'''

BACKUP_DIR = f"{ROOT_DIR}\\backup"
'''Путь к папке с бекапами БД'''

SKUD_DB_NAME = "SKUD.db"
'''Название базы данных СКУДа'''

VISITS_DB_NAME = "visits.db"
'''Название базы данных СКУДа'''

SKUD_SCRIPT_PATH = f"{ROOT_DIR}\\dbscripts\\skud_script.sql"
'''Путь к скрипту, создающему базу данных СКУДа'''

VISITS_SCRIPT_PATH = f"{ROOT_DIR}\\dbscripts\\visits_script.sql"
'''Путь к скрипту, создающему базу данных посещений'''

ARDUINO_PORTS = ["COM7"]
'''Список портов, к которым присоединены платы'''

URL = "localhost", 8080
'''Временный адрес для проверки работы вебсервера'''

ROOM_PORT_MAP = {0:"COM7"}