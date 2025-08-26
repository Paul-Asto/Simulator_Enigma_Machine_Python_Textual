from textual.message import Message
from src.core.types import DictDinamicConfEnigm


class EventDeletConfigRotor(Message):
    def __init__(self, index: int) -> None:
        super().__init__()
        
        self.index: int = index



class EventChangesInConfig(Message):

    def __init__(self) -> None:
        super().__init__()



class EventReEncript(Message):

    def __init__(self, config: DictDinamicConfEnigm) -> None:
        super().__init__()
        
        self.config: DictDinamicConfEnigm = config