from datetime import datetime

class HistoryRow:
    def __init__(self, port: str, message: str):
        self.port = port
        self.message = message
        self.pass_time = str(datetime.now().isoformat())