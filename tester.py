# import websocket
# #import thread
# import time

# def on_data(ws, message):
#     print(type(message))
#     print(message)

# def on_error(ws, error):
#     print(error)

# def on_close(ws, s, a):
#     print("### closed ###")

# def on_open(ws):
#     def run(*args):
#         for i in range(30000):
#             time.sleep(1)
#             ws.send("Hello %d" % i)
#         time.sleep(1)
#         ws.close()
#         print("thread terminating...")
#     #thread.start_new_thread(run, ())


# websocket.enableTrace(True)
# ws = websocket.WebSocketApp("ws://localhost:8080",
#                             on_data = on_data,
#                             on_error = on_error,
#                             on_close = on_close, 
#                             on_open = on_open)

# ws.run_forever()

from websocket import create_connection

ws = create_connection("ws://localhost:8080")

while True:
    msg = input('Enter a message: ')
    if msg == 'quit':        
        ws.close()
        break
    ws.send(msg)
    result =  ws.recv()
    print ('> ', result)