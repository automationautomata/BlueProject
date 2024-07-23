
import datetime
import json
from time import sleep
import schedule
from threading import Timer
# try:
#     from ORM.database import DatabaseConnection
#     from hardware.arduino import ArduinoCommunicator
# except:
#     import os
#     import sys
#     sys.path.append(os.path.dirname(os.path.dirname((os.path.realpath(__file__)))))
#     from ORM.database import DatabaseConnection
#     from hardware.arduino import ArduinoCommunicator

# def sendoutcards(arduino_room_map: list[tuple[int, ArduinoCommunicator]], SKUDdbConn: DatabaseConnection):
#     SKUDdbConn.establish_connection()
#     sql = '''SELECT room, card from entities inner join access_rules 
#                             on entities.right = access_rules.right group by room'''
#     data = SKUDdbConn.execute(sql)
    
#     for room, arduino in arduino_room_map:
#         getcards = lambda pair: pair[0] == room
#         cards = list(filter(getcards, data))
#         arduino.communicate(json.dump([pair[1] for pair in cards]))

def sendkey_deferred(arduino, key, time: datetime.datetime):
    defer = (datetime.datetime.now() - time).total_seconds()
    def deletekey():
        print(key)
        return schedule.CancelJob

    t.start()

sendkey_deferred(None, 452, datetime.datetime.now() + datetime.timedelta(seconds=20))
print('ddd2d')

sendkey_deferred(None, 3, datetime.datetime.now() + datetime.timedelta(seconds=17))
print('dddd')
def job_that_executes_once():
    print("dddddd")
    return schedule.CancelJob

schedule.every().day.at('01:01:30').do(job_that_executes_once)
while True:
    schedule.run_pending()
    sleep(0.1)