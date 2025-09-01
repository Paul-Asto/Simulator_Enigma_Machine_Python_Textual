from textual.message import Message
from src.core.config import DictDinamicConfig



class EventReEncript(Message):

    def __init__(self, config: DictDinamicConfig) -> None:
        super().__init__()
        
        self.config: DictDinamicConfig = config