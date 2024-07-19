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
import serial
import serial.tools.list_ports
def getportsinfo() -> str:
    '''Возвращает информацию обо всех COM портах в json-подобном виде'''
    ports = list(serial.tools.list_ports.comports())
    getinfo = lambda port: '{'+f"\"Port\": \"{port.device}\",\"Description\": \"{port.description}\", Manufacturer: \"{port.manufacturer}\""+'}'
    return f"{{',\n'.join(getinfo(port) for port in ports)}}"

# Открываем Serial порт ('COMX' замените на имя вашего порта)
def communicate(port: str, data: str, baudrate: int = 9600):
    ''''''
    ser = serial.Serial(port, baudrate)
    # Отправляем строку "Hello, Arduino!" на Arduino, предварительно преобразовав ее в байты
    #ser.write(b'Hello, Arduino!')
    ser.write(data)
    # Читаем ответ от Arduino через Serial порт
    response = ser.readline()
    # Декодируем ответ из байтов в строку с использованием UTF-8
    decoded_response = response.decode('utf-8')
    # Закрываем порт
    ser.close()
    return decoded_response
