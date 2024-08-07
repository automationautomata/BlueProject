import json
from datetime import datetime

class VisitsHistory:
    def __init__(self, port: str, message: str):
        self.port = port
        self.message = message
        self.pass_time = str(datetime.now().isoformat())
    def toJSON(self):
        return json.dump(self.__dict__)
    
class RemoteSessions:
    def __init__(self, address: str, token: int, event: str, message: str):
        self.address = address
        self.token = token
        self.event = event
        self.message = message
        self.sign_in_time = str(datetime.now().isoformat())
    def toJSON(self):
        return json.dump(self.__dict__)
    