import sqlite3
connection = sqlite3.connect(".\\DB\\SKUD")
cursor = connection.cursor()
# Создаем базу
with open(".\\dbscripts\\skud_script.sql", "r+") as scriptfile:
    script = scriptfile.read()
    cursor.executescript(script)
    connection.commit()