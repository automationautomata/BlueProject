from datetime import datetime

class VisitsHistory:
    def __init__(self, port: str, message: str):
        self.port = port
        self.message = message
        self.pass_time = str(datetime.now().isoformat())