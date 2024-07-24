import asyncio
from threading import Thread
import time
try:
    from SKUD.hardware.arduino import ArduinoCommunicator, create_listeners_thread
except:
    import os
    import sys
    sys.path.append(os.getcwd())
    from SKUD.hardware.arduino import ArduinoCommunicator, create_listeners_thread

############################### ПРИМЕР 1 ###############################

def example1():
    ard = ArduinoCommunicator('COM7', handler=lambda x: print(x, 'COM7'))
    ard2 = ArduinoCommunicator('COM6', handler=lambda x: print(x,'COM6'))
    def test():
        async def ini():  
            tasks = []
            tasks.append(asyncio.create_task(ard.listener(0.005)))
            tasks.append(asyncio.create_task(ard2.listener(0.004)))
            # loop = asyncio.get_event_loop()
            # asyncio.set_event_loop(loop)
            await asyncio.gather(*tasks)
        asyncio.run(ini())

    print('COM7 connection: ', ard.connection.is_open, ', COM6 connection: ',  ard2.connection.is_open)
    Thread(target=test, daemon=True).start()

    ard2.write("{\"hello\": \"6\"}")
    time.sleep(2)

    ard2.write("{\"hello\": \"6 2\"}")
    ard.write("{\"hello\": \"7\"}")
    time.sleep(3)

    print('COM7 connection: ', ard.connection.is_open, ', COM6 connection: ',  ard2.connection.is_open)
    print("END")

############################### ПРИМЕР 2 ###############################

def example2():
    ard = ArduinoCommunicator('COM7', handler=lambda x: print(x, 'COM7'))
    ard2 = ArduinoCommunicator('COM6', handler=lambda x: print(x,'COM6'))
    t = create_listeners_thread([ard, ard2])

    print('COM7 connection: ', ard.connection.is_open, ', COM6 connection: ',  ard2.connection.is_open)
    t.start()

    ard2.write("{\"hello\": \"6\"}")
    time.sleep(2)

    ard2.write("{\"hello\": \"6 2\"}")
    ard.write("{\"hello\": \"7\"}")
    time.sleep(3)

    print('COM7 connection: ', ard.connection.is_open, ', COM6 connection: ',  ard2.connection.is_open)
    print("END")

example1()