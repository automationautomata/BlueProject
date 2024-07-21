class DbAnswer:
    def __init__(self, answer_type: str, data: list[tuple], error: str) -> None:
        self.answer_type = answer_type
        self.data = convert(data)
        self.error = error
        
def convert(data: list[tuple]) -> list[list]:
    return [list(d) for d in data]

