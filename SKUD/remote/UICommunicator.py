import tornado

class SkudQueryHandler(tornado.web.RequestHandler):
    def initialize(self, actions_router):
        self.actions_router = actions_router

    def get(self):
        data, error = self.actions_router[self.get_body_argument("action")](self.get_body_argument("data"))
        self.write("{"+f"\"data\": \"{data}\", \"error\": \"{error}\""+"}")

    def post(self):
        _, error = self.actions_router[self.get_body_argument("action")](self.get_body_argument("data"))
        self.set_header("Content-Type", "text/plain")
        self.write("{"+f"\"error\": \"{error}\""+"}")

    def put(self):
        _, error = self.actions_router[self.get_body_argument("action")](self.get_body_argument("data"))
        self.set_header("Content-Type", "text/plain")
        self.write("{"+f"\"error\": \"{error}\""+"}")

    def delete(self):
        _, error = self.actions_router[self.get_body_argument("action")](self.get_body_argument("data"))
        self.set_header("Content-Type", "text/plain")
        self.write("{"+f"\"error\": \"{error}\""+"}")

class CardControllerWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")