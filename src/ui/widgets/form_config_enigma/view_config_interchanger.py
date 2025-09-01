from typing import Generator, cast
from textual.widget import Widget
from textual import on
from textual.widgets import Static, Select, Button
from textual.containers import  Vertical, Horizontal

from src.core.constants import ABC
from src.ui.widgets.form_config_enigma.event_changes_in_config import EventChangesInConfig



class ViewConfigInterchanges(Widget):
    
    DEFAULT_CSS = '''
    ViewConfigInterchanges{
        height: 4;
        width: 110;
        margin: 1 0;
    }
    
    ViewConfigInterchanges Vertical.content{
        height: 4;
        width: 110;
        border: solid;
    }
    
    ViewConfigInterchanges Horizontal.content{
        height: 3;
        width: 110;
        align-horizontal: center;
    }
    
    ViewConfigInterchanges  Select.select-abc{
    margin-left: 1;
    height: 1;
    width: 7;
    text-align: center;
    }
    
    ViewConfigInterchanges Button{
    margin-left: 2;
    height: 1;
    min-width: 7;
    width: 7;
    }
    
    ViewConfigInterchanges Static.data{
    margin-right: 5;
    height: 1;
    width: 60;
    background: gray;
    }
    
    ViewConfigInterchanges Static.title{
        text-align: center;
    }
    '''
    
    def __init__(self) -> None:
        super().__init__()
        
        self.__list_chars: list[str] = list(ABC)
        
        self.__title = Static("Interchangers", classes="title")
        self.__data = Static(classes="data")
        
        self.__select_a: Select[str] = Select([
            (char, char)
            for char in self.__list_chars
        ], compact=True, allow_blank=False, classes="select-abc")
        
        self.__select_b: Select[str] = Select([
            (char, char)
            for char in self.__list_chars
        ], compact=True, allow_blank= False, classes="select-abc")
        
        self.__button_add = Button("Add", id="add", compact= True)
        self.__button_clear = Button("Clear", id="clear", compact= True)
    
    
    @property
    def data_interchangers(self) -> list[tuple[str, str]]:
        data: str = str(self.__data.render())
        if data == "": return []
        return [(d[0], d[1])for d in data.strip().split(" ")]
    
    
    def compose(self) -> Generator[Widget, None, None]:
        with Vertical(classes="content"):
            yield self.__title
            
            with Horizontal(classes="content"):
                yield self.__data
                yield self.__select_a
                yield self.__select_b
                yield self.__button_add
                yield self.__button_clear
    
    
    @on(Button.Pressed, "#add")
    def add_interchanger(self) -> None:
        value_a: str = cast(str, self.__select_a.value)
        value_b: str = cast(str, self.__select_b.value)
        
        if value_a == value_b:
            return
        
        data = self.__data.render()
        self.__data.update(f"{data} {value_a}{value_b}")
        
        self.__list_chars.remove(value_a)
        self.__list_chars.remove(value_b)
        
        self.__update_options()
        self.post_message(EventChangesInConfig())
    
    
    @on(Button.Pressed, "#clear")
    def clear_interchangers(self) -> None:
        self.__data.update()
        self.__list_chars = list(ABC)
        self.__update_options()
        self.post_message(EventChangesInConfig())
    
    
    def __update_options(self) -> None:
        self.__select_a.set_options([
            (char, char)
            for char in self.__list_chars
        ])
        
        self.__select_b.set_options([
            (char, char)
            for char in self.__list_chars
        ])