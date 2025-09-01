from typing import Generator, Iterable
from textual.widget import Widget
from textual import on
from textual.widgets import Static, Select
from textual.containers import  Vertical

from src.ui.widgets.form_config_enigma.event_changes_in_config import EventChangesInConfig



class SelectModel(Widget):
    DEFAULT_CSS = '''
    SelectModel{
        width: 30;
        height: 4;
        border: solid;
    }
    SelectModel Static.title{
        text-align: center;
    }
    
    SelectModel Select.select-model Static{
        text-align: center;
    }
    '''
    
    def __init__(self, title: str, classes: str = "", content: Iterable[str] = []) -> None:
        super().__init__(classes= classes)
        
        self.__title = Static(title, classes="title")
        self.__select: Select[str] = Select([
            (d, d) 
            for d in content
        ], allow_blank= False, compact= True, classes="select-model")
    
    
    @property
    def value(self) -> str:
        return str(self.__select.value)
    
    
    def compose(self) -> Generator[Widget, None, None]:
        with Vertical(classes="content"):
            yield self.__title
            yield self.__select
    
    
    def update_title(self, new_title: str):
        self.__title.update(new_title)
    
    
    @on(Select.Changed)
    def on_select_changed(self, event: Select.Changed) -> None:
        self.post_message(EventChangesInConfig())
