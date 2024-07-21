
import json
from ORM.database import DatabaseConnection
from hardware.arduino import ArduinoCommunicator


def sendoutcards(arduino_room_map: list[tuple[int, ArduinoCommunicator]], SKUDdbConn: DatabaseConnection):
    SKUDdbConn.establish_connection()
    sql = '''SELECT room, card from entities inner join access_rules 
                            on entities.right = access_rules.right group by room'''
    data = SKUDdbConn.execute(sql)
    
    for room, arduino in arduino_room_map:
        getcards = lambda pair: pair[0] == room
        cards = list(filter(getcards, data))
        arduino.communicate(json.dump([pair[1] for pair in cards]))

def recieve_event():
    