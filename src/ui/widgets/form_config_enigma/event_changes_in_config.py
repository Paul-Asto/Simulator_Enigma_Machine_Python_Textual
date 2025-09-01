from textual.message import Message


class EventChangesInConfig(Message):

    def __init__(self) -> None:
        super().__init__()