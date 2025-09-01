from textual.message import Message


class EventDeletConfigRotor(Message):
    def __init__(self, index: int) -> None:
        super().__init__()
        
        self.index: int = index