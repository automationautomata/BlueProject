# import os.path
# from abc import ABC, abstractmethod

# # class HardwareConnection(ABC):
# #     @abstractmethod
# #     def EstablishConnection() -> None: pass
# #     @abstractmethod
# #     def send(data) -> bool: pass
# #     @abstractmethod
# #     def recieve() -> str: pass

# # class CardChecker(HardwareConnection):
# #     def EstablishConnection() -> None: pass
# #     def send(data) -> bool: pass
# #     def recieve() -> str: pass

import time
from typing import Any, Callable
import serial
import serial.tools.list_ports
import os
import sys

try:
    from ORM.logger import Logger
    from config import ARDUINO_PORT
except:
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname((os.path.realpath(__file__)))))
    from ORM.logger import Logger
    from config import ARDUINO_PORT

def getportsinfo() -> str:
    '''Возвращает информацию обо всех COM портах в json-подобном виде'''
    ports = list(serial.tools.list_ports.comports())
    getinfo = lambda port: '{'+f"\"Port\": \"{port.device}\",\
                                 \"Description\": \"{port.description}\", \
                                 \"Manufacturer\": \"{port.manufacturer}\""+'}'
    return '{'+f"{',\n'.join(getinfo(port) for port in ports)}"+'}'

# Синхронное общение
class ArduinoCommunicator:
    '''Класс для отправки данных на ардуино'''
    def __init__(self, port: str, format_send: Callable[[Any], str] = None, logger: Logger = None, baudrate: int = 9600) -> None:
        '''`port` - номер COM порта, `format_send` - функция, превращающая входные данные в строку, 
        `logger` - сохраняет ошибки и доп.информацию в БД, `baudrate` - частота'''
        self.connection = serial.Serial(port, baudrate)
        self.logger = logger
        self.format_send = format_send
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

    def communicate(self, data: str) -> str | None:
        '''Отправляет данные в формате строки на ардуино и возвращает ответ от него, 
        если соединение закрыто, то открывает его заново'''
        try:
            if not self.connection.is_open:
                self.connection.open()
            #ser = serial.Serial(port, baudrate)
            # Отправляем строку "Hello, Arduino!" на Arduino, предварительно преобразовав ее в байты
            #ser.write(b'Hello, Arduino!')
            #self.connection.write(data.encode())
            # Читаем ответ от Arduino через Serial порт
            response = self.connection.read_all()
            print(response)
            # Декодируем ответ из байтов в строку с использованием UTF-8
            #decoded_response = 
            return response.decode('utf-8')
        except NameError: 
            if self.logger:
                self.logger.addlog(f"In ArduinoCommunicator.communicate() with input data: {data} ERROR: {NameError}")
            print(NameError)
    def close(self):
        # Закрываем порт
        self.connection.close()
        
## ТЕСТ
ard = ArduinoCommunicator(ARDUINO_PORT[0])
#print(ard.communicate("{\"hello\": \"COM\"}"))
response = ard.connection.readline()
response = ard.connection.readline()
print(response)
# response = ard.connection.read_all()
# print(response)
# response = ard.connection.read_all()
# print(response)
time.sleep(2)
# ard.close()