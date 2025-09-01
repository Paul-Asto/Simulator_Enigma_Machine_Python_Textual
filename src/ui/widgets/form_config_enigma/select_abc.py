from typing import Generator
from textual.widget import Widget
from textual import on
from textual.widgets import Static, Button
from textual.containers import Horizontal

from src.core.utilities import from_index_to_letter
from src.core.constants import SIZE_ABC
from src.ui.widgets.form_config_enigma.event_changes_in_config import EventChangesInConfig


class SelectAbc(Widget):
    
    DEFAULT_CSS = '''
    SelectAbc{
        width: 30;
        height: 4;
        border: solid;
    }
    
    Static.data-abc{
        text-align: center;
        width: 8;
    }
    
    Button.minus{
        min-width: 7;
        width: 7;
    }
    
    Button.plus{
        min-width: 7;
        width: 7;
    }
    
    SelectAbc Static.title{
        text-align: center;
    }
    
    SelectAbc Horizontal.content{
        align-horizontal: center;
    }
    
    '''
    
    def __init__(self, title: str, index: int = 0) -> None:
        super().__init__()
        
        self.__index: int = index
        self.__title = Static(title, classes= "title")
        self.__button_minos = Button("-", classes="minus", compact= True)
        self.__data = Static(classes="data-abc")
        self.__button_plus = Button("+", classes="plus", compact= True)
        
        self.__update_data()
    
    
    @property
    def value(self) -> str:
        return from_index_to_letter(self.__index)
    
    
    def compose(self) -> Generator[Widget, None, None]:
        yield self.__title
        with Horizontal(classes="content"):
            yield self.__button_minos
            yield self.__data
            yield self.__button_plus
    
    
    @on(Button.Pressed, ".plus")
    def plus(self) -> None:
        new_index: int = self.__index + 1
        self.__index = new_index % SIZE_ABC 
        self.__update_data()
        self.post_message(EventChangesInConfig())
    
    
    @on(Button.Pressed, ".minus")
    def minus(self) -> None:
        new_index: int = self.__index - 1
        self.__index = new_index \
            if new_index >= 0 else \
            SIZE_ABC - (abs(new_index) % SIZE_ABC)
        self.__update_data()
        self.post_message(EventChangesInConfig())
    
    
    def __update_data(self):
        self.__data.update(f"{self.__index + 1} {from_index_to_letter(self.__index)}")
