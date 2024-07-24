# # import os.path
# # from abc import ABC, abstractmethod

# # # class HardwareConnection(ABC):
# # #     @abstractmethod
# # #     def EstablishConnection() -> None: pass
# # #     @abstractmethod
# # #     def send(data) -> bool: pass
# # #     @abstractmethod
# # #     def recieve() -> str: pass

# # # class CardChecker(HardwareConnection):
# # #     def EstablishConnection() -> None: pass
# # #     def send(data) -> bool: pass
# # #     def recieve() -> str: pass

import asyncio
from threading import Thread
import time
from typing import Any, Callable
import serial
import serial.tools.list_ports

try:
    from ORM.logger import Logger
    from config import ARDUINO_PORT
except:
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname((os.path.realpath(__file__)))))
    from ORM.logger import Logger
    from config import ARDUINO_PORT

# def getportsinfo() -> str:
#     '''Возвращает информацию обо всех COM портах в json-подобном виде'''
#     ports = list(serial.tools.list_ports.comports())
#     getinfo = lambda port: '{'+f"\"Port\": \"{port.device}\",\
#                                  \"Description\": \"{port.description}\", \
#                                  \"Manufacturer\": \"{port.manufacturer}\""+'}'
#     return '{'+f"{',\n'.join(getinfo(port) for port in ports)}"+'}'

# Синхронное общение
class ArduinoCommunicator:
    '''Класс для отправки данных на ардуино'''
    def __init__(self, **kwargs) -> None:
        '''`port` - номер COM порта, `format_send` - функция, превращающая входные данные в строку, 
        `logger` - сохраняет ошибки и доп.информацию в БД, `baudrate` - частота'''
        self.connection = serial.Serial(kwargs["port"], kwargs["baudrate"])
        self.logger = kwargs["logger"]
        self.handler = kwargs["handler"]
        self.format_send = kwargs["format_send"]
        self.endflag = kwargs["endflag"]
        self.startflag = kwargs["startflag"]

    def __init__(self, port: str, handler: Callable[[bytes], None], startflag: str = "{", endflag: str = "}", format_send: Callable[[Any], str] = None, 
                 logger: Logger = None, baudrate: int = 9600) -> None:
        '''`port` - номер COM порта, `format_send` - функция, превращающая входные данные в строку, 
        `logger` - сохраняет ошибки и доп.информацию в БД, `baudrate` - частота'''
        self.connection = serial.Serial(port, baudrate)
        self.logger = logger
        self.handler = handler
        self.format_send = format_send
        self.endflag = endflag
        self.startflag = startflag
        #### self.format_receive = format_receive - нужно ???

    def communicate_format(self, data: Any):
        '''Отправляет данные в формате строки, полученной с помощью `format_send` на ардуино 
        и возвращает ответ от него, если соединение закрыто, то открывает его заново'''
        try:
            return self.communicate(self.format_send(data))
        except NameError: 
            if self.logger:
                self.logger.addlog(f"In ArduinoCommunicator.communicate() with input data: {data} ERROR: {NameError}")
            print(NameError)

    def write(self, data: str) -> str | None:
        '''Отправляет данные в формате строки на ардуино и возвращает ответ от него, 
        если соединение закрыто, то открывает его заново'''
        try:
            if not self.connection.is_open:
                self.connection.open()
            #ser = serial.Serial(port, baudrate)
            # Отправляем строку "Hello, Arduino!" на Arduino, предварительно преобразовав ее в байты
            #ser.write(b'Hello, Arduino!')
            return self.connection.write(data.encode())
            # Читаем ответ от Arduino через Serial порт
            # response = self.connection.read_until()
            # print(response)
            # # Декодируем ответ из байтов в строку с использованием UTF-8
            # #decoded_response = 
            # return response.decode('utf-8')
        except NameError: 
            if self.logger:
                self.logger.addlog(f"In ArduinoCommunicator.communicate() with input data: {data} ERROR: {NameError}")
            print(NameError)

    async def listener(self) -> None:
        await asyncio.sleep(0.1)
        while self.connection.is_open:
            #print(ard.connection.in_waiting)
            if self.connection.in_waiting > 0:
                start_symb = self.connection.read(1)
                print(start_symb.decode('utf-8'), self.startflag)
                if start_symb.decode('utf-8') == self.startflag:
                    response = self.connection.read_until(expected=self.endflag.encode())
                    print(self.connection.port, start_symb.decode('utf-8') + response.decode('utf-8'))
                    self.handler(start_symb + response)
            self.connection.reset_input_buffer()
        #ard.connection.reset_input_buffer()
    def close(self):
        # Закрываем порт
        self.connection.close()

def start_multiple_listeners(arduinos: list[ArduinoCommunicator]):
    def thread_func(): 
        asyncio.run(arduinos[0].listener())
    thread = Thread(target=thread_func, daemon=True)
    return arduinos, thread
################ ТЕСТ ################
# ard = ArduinoCommunicator(ARDUINO_PORT[0], handler=lambda x: print(x.decode('utf-8') + "ddd"))
# ard2 = ArduinoCommunicator('COM1', handler=lambda x: print(x.decode('utf-8')))
# def ini():
#     asyncio.gather(ard.listener(), ard2.listener())
# print(ard.connection.is_open)
# t = Thread(target=ini, daemon=True)
# t.start()
# time.sleep(1)
# print(ard.connection.is_open)
ard = ArduinoCommunicator(ARDUINO_PORT[0], handler=lambda x: print(x.decode('utf-8') + "ddd"))
fn = handler=lambda x: print(x.decode('utf-8') + "ddd")
ards, t = start_multiple_listeners([ard])
t.start()
time.sleep(5)
print('\\')
ard.write("{\"hello\": \"COM\"}")
time.sleep(10)
# t.join()
## ТЕСТ
# ard = ArduinoCommunicator(ARDUINO_PORT[0])
# #print(ard.communicate("{\"hello\": \"COM\"}"))
# response = ard.connection.readline()
# print(response)
# while True:
#     print(ard.connection.in_waiting)
#     if ard.connection.in_waiting > 10:
#         ard.connection.reset_input_buffer()
#         break
# ard.connection.reset_input_buffer()

# print(ard.connection.in_waiting)
# response = ard.connection.readline()
# print(response)
# response = ard.connection.read_all()
# print(response)
# response = ard.connection.read_all()
# print(response)
# time.sleep(20)
# ard.close()

# from threading import Thread, Timer
# import time
# from typing import Any, Callable
# import serial.tools.list_ports
# import asyncio
# import serial_asyncio

# try:
#     from ORM.logger import Logger
#     from config import ARDUINO_PORT
# except:
#     import os
#     import sys
#     sys.path.append(os.path.dirname(os.path.dirname((os.path.realpath(__file__)))))
#     from ORM.logger import Logger
#     from config import ARDUINO_PORT

# def getportsinfo() -> str:
#     '''Возвращает информацию обо всех COM портах в json-подобном виде'''
#     ports = list(serial.tools.list_ports.comports())
#     getinfo = lambda port: '{'+f"\"Port\": \"{port.device}\",\
#                                  \"Description\": \"{port.description}\", \
#                                  \"Manufacturer\": \"{port.manufacturer}\""+'}'
#     return '{'+f"{',\n'.join(getinfo(port) for port in ports)}"+'}'

# class ArduinoCommunicator:
#     '''Класс для отправки данных на ардуино'''
#     class OutputProtocol(asyncio.Protocol):
#         def __init__(self) -> None:
#             self.answer: Callable[[bytes], str | None] = None
#             self.close_cond: Callable[[str], str] = None
#             self.logger: Callable[[str], str] = None
#             self.format:  Callable[[Any], str] = None
#             super().__init__()

#         def connection_made(self, transport):
#             self.transport = transport
#             print('port opened', transport)
#             transport.serial.rts = False  # You can manipulate Serial object via transport
#             #transport.write(b'{\"hello\": \"COM\"}')  # Write serial data via transport

#         def data_received(self, data):
#             print('data received', repr(data))
#             msg = self.answer(data)
#             if msg: self.transport.write(msg)

#             # if self.close_cond(data):
#             #     self.transport.close()

#         def write(self, data: str):
#             '''Отправляет данные в формате строки на ардуино и возвращает ответ от него, 
#             если соединение закрыто, то открывает его заново'''
#             self.transport.write(data.encode())

#         def write_format(self, data: Any):
#             '''Отправляет данные в формате строки, полученной с помощью `format` на ардуино 
#             и возвращает ответ от него, если соединение закрыто, то открывает его заново'''
#             if self.format:
#                 self.write(self.format(data))
#             else:
#                 raise Exception("format function in None")
            
#         def connection_lost(self, exc):
#             print('port closed')
#             self.transport.loop.stop()

#         def pause_writing(self):
#             print('pause writing')
#             print(self.transport.get_write_buffer_size())

#         def resume_writing(self):
#             print(self.transport.get_write_buffer_size())
#             print('resume writing')
    
#     def __init__(self, port: str, answer: Callable[[bytes], str | None], close_cond: Callable[[str], str], format: Callable[[Any], str] = None, 
#                  logger: Logger = None, baudrate: int = 9600) -> None:
#         '''`port` - номер COM порта, `format_send` - функция, превращающая входные данные в строку, 
#         `logger` - сохраняет ошибки и доп.информацию в БД, `baudrate` - частота'''
#         self.logger = logger
#         self.format = format
        
#         self.loop = asyncio.get_event_loop()
#         self.coro = serial_asyncio.create_serial_connection(self.loop, ArduinoCommunicator.OutputProtocol, port, baudrate=baudrate)
#         self.transport, self.protocol = self.loop.run_until_complete(self.coro)
#         self.protocol.answer = answer
#         self.protocol.close_cond = close_cond
#         # transport.write(b'{\"hello\": \"COM4\"}')
#         # self.loop.run_forever()
#     def start(self): 
#         # self.transport, self.protocol = self.loop.run_until_complete(self.coro)
#         # self.protocol.answer = answer
#         # self.protocol.close_cond = close_cond
#         # transport.write(b'{\"hello\": \"COM4\"}')
#         return 

#     def write(self, data):
#         self.protocol.write(data)
        
#     def close(self): 
#         '''Закрывает соединение'''
#         self.loop.stop()
#         self.loop.close()




# from asyncio import get_event_loop
# from serial_asyncio import open_serial_connection

# async def run(h):
#     ser = serial.Serial(port='COM6', baudrate=9600)

#     while True:
#         line = ser.readline()
#         if line:
#             print(str(line, 'utf-8'))

#             if str(line, 'utf-8') == "END":
#                 break
#             r = h(str(line, 'utf-8'))
#             if r: 
#                 ser.write(r)

# async def run2(h):
#     ser = serial.Serial(port='COM1', baudrate=9600)

#     while True:
#         line = ser.readline()
#         if line:
#             print(str(line, 'utf-8'))

#             if str(line, 'utf-8') == "END":
#                 break
#             r = h(str(line, 'utf-8'))
#             if r: 
#                 ser.write(r)

# loop = get_event_loop()
# get = "{\"hello\": \"COM\"}"
# def h(s):
#     return get.encode() if get else None
# def h2(s):
#     return get.encode() if get else None
# asyncio.run(run(h))
# get = None

# print("ssss")

# def job():
#     print("I'm working...")

# t = Timer(3, job)
# t.start()