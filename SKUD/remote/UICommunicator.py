import tornado
from threading import Thread

class SkudQueryHandler(tornado.web.RequestHandler):
    def initialize(self, actions):
        self.actions = actions

    def get(self):
        data, error = self.actions[self.get_body_argument("action")](self.get_body_argument("data"))
        self.write("{"+f"\"data\": \"{data}\", \"error\": \"{error}\""+"}")

    def post(self):
        error = self.actions[self.get_body_argument("action")](self.get_body_argument("data"))
        self.set_header("Content-Type", "text/plain")
        self.write("{"+f"\"error\": \"{error}\""+"}")

    def put(self):
        error = self.actions[self.get_body_argument("action")](self.get_body_argument("data"))
        self.set_header("Content-Type", "text/plain")
        self.write("{"+f"\"error\": \"{error}\""+"}")

    def delete(self):
        error = self.actions[self.get_body_argument("action")](self.get_body_argument("data"))
        self.set_header("Content-Type", "text/plain")
        self.write("{"+f"\"error\": \"{error}\""+"}")

class visits_dbWebSocket(tornado.websocket.WebSocketHandler):
    def initialize(self, actions):
        self.actions = actions
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")

def make_server_thread(http_handler_type, ws_handler_type, port, actions, isdaemon=True) -> tuple[Thread, tornado.web.Application]:
    app = tornado.web.Application([
        (r"/", http_handler_type, dict(actions=actions)),
        (r"/websocket", ws_handler_type, dict(actions=actions)),
    ])
    app.listen(port)
    return Thread(tornado.ioloop.IOLoop.current().start, daemon=isdaemon), app