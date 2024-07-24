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
    def __init__(self, **kwargs) -> None:
        '''`port` - номер COM порта, `format_send` - функция, превращающая входные данные в строку, 
        `logger` - сохраняет ошибки и доп.информацию в БД, `baudrate` - частота'''
        self.connection = serial.Serial(kwargs["port"], kwargs["baudrate"])
        self.logger = kwargs["logger"]
        self.handler = kwargs["handler"]
        self.format_send = kwargs["format_send"]
        self.endflag = kwargs["endflag"]
        self.startflag = kwargs["startflag"]

    def __init__(self, port: str, handler: Callable[[bytes], str], startflag: str = "{", endflag: str = "}", format_send: Callable[[Any], str] = None, 
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

    async def listener(self, timeout):
        '''Слушает порт, если в буффер не пуст и первый символ совпадает со `startflag`, то читает до `endflag` и отправляет 
        принятое сообщение в функцию `handler` (она вернет строку, то она будет отправлена как ответ).
        Если первый символ не совпадает, то буфер отчищается.'''
        while self.connection.is_open:
            await asyncio.sleep(timeout)
            #print(self.connection.port)  
            if self.connection.in_waiting > 0:
                start_symb = self.connection.read(1)
                #print(ard.connection.port, start_symb.decode('utf-8'), ard.startflag)
                if start_symb.decode('utf-8') == self.startflag:
                    response = self.connection.read_until(expected=self.endflag.encode())
                    #print(ard.connection.port, start_symb.decode('utf-8') + response.decode('utf-8'), start_symb + response)
                    response = self.handler(start_symb + response)
                    #response = await self.handler(start_symb + response)
                    if response:
                        self.connection.write(response.encode())
                else: self.connection.reset_input_buffer()
    def close(self):
        # Закрываем порт
        self.connection.close()

def create_listeners_thread(arduinos: list[ArduinoCommunicator], start_sleep_time: int = 0,  delta: int = 0.001):
    '''Создает поток, асинхронно выполняющий прослушивание портов, `arduinos` - подключенные устройства,
    `start_sleep_time` - время сна первой функции, `delta` - дельта между временем сна двух функций'''
    async def ini():
        tasks = [asyncio.create_task(ard.listener(start_sleep_time + ind*delta)) for ind, ard in enumerate(arduinos)]
        await asyncio.gather(*tasks)
    thread = Thread(target=lambda:asyncio.run(ini()), daemon=True)
    return thread
