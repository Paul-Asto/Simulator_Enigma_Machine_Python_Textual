from typing import Generator, TYPE_CHECKING
from textual.widget import Widget
from textual import on
from textual.widgets import  Button
from textual.containers import Horizontal

from src.core.constants import  MODELS_ROTOR
from src.ui.widgets.form_config_enigma.select_abc import SelectAbc
from src.ui.widgets.form_config_enigma.select_model import SelectModel

from src.ui.widgets.form_config_enigma.event_changes_in_config import EventChangesInConfig
from src.ui.widgets.form_config_enigma.event_delet_config_rotor import EventDeletConfigRotor

if TYPE_CHECKING:
    from src.ui.widgets.form_config_enigma.container_config_rotor import ContainerConfigRotor



class ViewConfigRotor(Widget):
    DEFAULT_CSS = '''
    ViewConfigRotor{
        height: 4;
    }
    
    ViewConfigRotor Horizontal.content{
        align-horizontal: center
    }
    
    Button.delete{
        margin: 1 4;
        min-height: 3;
        min-width: 10;
    }
    '''
    
    def __init__(self, id: int, container: "ContainerConfigRotor") -> None:
        super().__init__()
        
        self.__index: int = id
        self.__select_type = SelectModel(f"Rotor {id}", content=MODELS_ROTOR)
        self.__select_position = SelectAbc("Posicion")
        self.__select_ring = SelectAbc("Ring")
        self.__delete_button = Button("Delete", classes="delete")
    
    
    @property
    def value_type(self) -> str:
        return self.__select_type.value
    
    
    @property
    def value_position(self) -> str:
        return self.__select_position.value
    
    
    @property
    def value_ring(self):
        return self.__select_ring.value
    
    
    def compose(self) -> Generator[Widget, None, None]:
        with Horizontal(classes="content"):
            yield self.__select_type
            yield self.__select_position
            yield self.__select_ring
            yield self.__delete_button
    
    
    @on(Button.Pressed, ".delete")
    def delete_rotor(self) -> None:
        self.post_message(EventDeletConfigRotor(self.__index))
        self.post_message(EventChangesInConfig())
    
    
    def update_title_rotor(self, id:int) -> None:
        self.__index = id
        self.__select_type.update_title(f"Rotor {id}")