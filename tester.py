# # import websocket
# # #import thread
# # import time

# # def on_data(ws, message):
# #     print(type(message))
# #     print(message)

# # def on_error(ws, error):
# #     print(error)

# # def on_close(ws, s, a):
# #     print("### closed ###")

# # def on_open(ws):
# #     def run(*args):
# #         for i in range(30000):
# #             time.sleep(1)
# #             ws.send("Hello %d" % i)
# #         time.sleep(1)
# #         ws.close()
# #         print("thread terminating...")
# #     #thread.start_new_thread(run, ())


# # websocket.enableTrace(True)
# # ws = websocket.WebSocketApp("ws://localhost:8080",
# #                             on_data = on_data,
# #                             on_error = on_error,
# #                             on_close = on_close, 
# #                             on_open = on_open)

# # ws.run_forever()

# # from websocket import create_connection

# # ws = create_connection("ws://localhost:8080")

# # while True:
# #     msg = input('Enter a message: ')
# #     if msg == 'quit':        
# #         ws.close()
# #         break
# #     ws.send(msg)
# #     result =  ws.recv()
# #     print ('> ', result)

# # import websocket

# # def on_message(wsapp, message):
# #     print(message)

# # wsapp = websocket.WebSocketApp("ws://localhost:8080", on_message=on_message)

# # wsapp.run_forever() 

# import json
# import websocket
# import config
# from typing import Callable

# from SKUD.database import AccessControl


# class UiCommunicator:
#     def __init__(self, router: dict[str, Callable[[str], str]], url="ws://localhost:8080") -> None:
#         self.url = url
#         self.router = router

#     def connect(self) -> None:
#         self.websocket = websocket.WebSocketApp(self.url, on_message=self.handler)
#         self.websocket.run_forever() 

#     def handler(self, ws: websocket.WebSocketApp, message: str) -> None:
#         print(message)
#         msg = json.loads(message)
#         func = self.router[msg['action']]
#         answer = func(msg['data'])
#         ws.send(answer)

# class Controller: 

#     def getentites(data: str) -> str:
#         db = AccessControl(config.SCRIPT_PATH, config.DB_NAME)
#         db.establish_connection(config.ROOT_DIR)
#         condition = " and ".join(f"{data["column"]} = {user}" for user in data["users"])
#         join_query = f"(select * from entities where {condition}) as e"
#         if data["extra"] == "rights":
#             join_query += " inner join rights on e.right = rights.right"
#         elif data["extra"] == "cards":   
#             join_query += " inner join cards on cards.id = e.card"
#         elif data["extra"] == "both":
#             join_query = f"(({join_query}inner join rights on e.right = rights.right) as er 
#                                             inner join cards on cards.id = er.card)"
#         result = db.execute(f'''select * from {join_query}''')
#         print(result)
#         return result
    
#     def createquery(main_table: str, join_tables: list[(str, str, str)] = None, 
#                     conditions: list[str] = None):
#         pass
#     def getaccessrules(rights):
#         db = AccessControl(config.SCRIPT_PATH, config.DB_NAME)
#         db.establish_connection(config.ROOT_DIR)
#         condition = " and ".join(f"sid = {right}" for right in rights)
#         db.execute(f'''select * from (((select * from access_rules where {condition}) as e 
#                                         inner join rights on e.right = rights.right) as er 
#                                             inner join cards on cards.id = er.card)''')

import time
import serial.tools.list_ports
# Получаем список доступных Serial портов
# ports = list(serial.tools.list_ports.comports())
# Выводим информацию о каждом порте
def getportsinfo() -> str:
    '''Возвращает информацию обо всех COM портах в json-подобном виде'''
    ports = list(serial.tools.list_ports.comports())
    getinfo = lambda port: '{'+f"\"Port\": \"{port.device}\", \"Description\": \"{port.description}\", \"Manufacturer\": \"{port.manufacturer}\""+'}'
    return '{'+f"{',\n'.join(getinfo(port) for port in ports)}"+'}'
print(getportsinfo())

# import serial
# # Открываем Serial порт ('COMX' замените на имя вашего порта)
# ser = serial.Serial('COM6', 9600)
# # Отправляем строку "Hello, Arduino!" на Arduino, предварительно преобразовав ее в байты
# ser.write(b'Hello, Arduino!')
# # Читаем ответ от Arduino через Serial порт
# response = ser.readline()
# # Декодируем ответ из байтов в строку с использованием UTF-8
# decoded_response = response.decode('utf-8')
# # Закрываем порт
# ser.close()
# print(decoded_response)

#time.sleep(10)

#git config --global core.autocrlf false
########################################