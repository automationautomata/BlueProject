import asyncio
import os
import sys
import serial
from typing import Callable
from threading import Thread
sys.path.append(os.path.dirname(os.path.dirname((os.path.realpath(__file__)))))
from hardware.arduino import ArduinoCommunicator

def getportsinfo() -> str:
    '''Возвращает информацию обо всех COM портах в json-подобном виде'''
    ports = list(serial.tools.list_ports.comports())
    getinfo = lambda port: '{'+f"\"Port\": \"{port.device}\",\
                                 \"Description\": \"{port.description}\", \
                                 \"Manufacturer\": \"{port.manufacturer}\""+'}'
    return '{'+f"{',\n'.join(getinfo(port) for port in ports)}"+'}'

def create_listeners_thread(arduinos: list[ArduinoCommunicator], 
                            start_sleep_time: int = 0,  delta: int = 0.001) -> Thread:
    '''Создает поток, асинхронно выполняющий прослушивание портов, `arduinos` - подключенные устройства,
    `start_sleep_time` - время сна первой функции, `delta` - дельта между временем сна двух функций'''
    async def ini():
        tasks = [asyncio.create_task(ard.listener(start_sleep_time + ind*delta)) for ind, ard in enumerate(arduinos)]
        await asyncio.gather(*tasks)
    thread = Thread(target=lambda:asyncio.run(ini()), daemon=True)
    return thread

def ardions_configuring(ports: list[str], 
                        handler: Callable[[bytes], str], handler_kwargs=None) -> tuple[Thread, dict[str, ArduinoCommunicator]]: 
    arduinos = {}
    for port in ports:
        arduinos[port] = ArduinoCommunicator(port=port, handler=handler, handler_kwargs=handler_kwargs)
    thread = create_listeners_thread(list(arduinos.values()))
    return thread, arduinos
