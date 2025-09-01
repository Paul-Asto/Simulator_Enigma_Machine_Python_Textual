from typing import Generator
from textual.widget import Widget
from textual.widgets import Static
from textual.containers import  Vertical

from src.core.constants import  MODELS_REFLECT
from src.core.config import DictConfigRotor, DictConfigInterchanger

from src.ui.widgets.form_config_enigma.select_model import SelectModel
from src.ui.widgets.form_config_enigma.container_config_rotor import ContainerConfigRotor
from src.ui.widgets.form_config_enigma.view_config_interchanger import ViewConfigInterchanges

from src.ui.events import  EventReEncript
from src.ui.widgets.form_config_enigma.event_changes_in_config import EventChangesInConfig



class ViewConfigEnigma(Widget):
    DEFAULT_CSS = '''
    ViewConfigEnigma{
    margin:1 3;
    border: solid;
    width: 112;
    height: 32;
    }
    
    ViewConfigEnigma Static.title{
        text-align: center;
    }
    
    '''
    
    
    def __init__(self) -> None:
        super().__init__()
        
        self.__title = Static("CONFIG ENIGMA", classes="title")
        self.__config_interchangers = ViewConfigInterchanges()
        self.__reflect_select = SelectModel("Reflect", content=MODELS_REFLECT)
        self.__container_config_rotor = ContainerConfigRotor()
    
    
    def compose(self) -> Generator[Widget, None, None]:
        with Vertical(classes="content"):
            yield self.__title
            yield self.__config_interchangers
            yield self.__reflect_select
            yield self.__container_config_rotor
    
    
    def on_event_changes_in_config(self, event: EventChangesInConfig) -> None:
        rotors: list[DictConfigRotor] =  [
            {
            "model": config.value_type,
            "position": config.value_position,
            "ring": config.value_ring,
            }
            for config in self.__container_config_rotor.list_view_config
        ]
        
        reflect: str = self.__reflect_select.value
        
        interchangers: list[DictConfigInterchanger] = [
            {"letter_a": a, "letter_b": b} 
            for a, b in self.__config_interchangers.data_interchangers
        ]
        
        self.post_message(EventReEncript({
            "rotors":  rotors,
            "reflect": reflect,
            "interchanger": interchangers
        }))
