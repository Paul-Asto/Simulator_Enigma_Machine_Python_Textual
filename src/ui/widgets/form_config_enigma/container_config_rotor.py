from typing import Generator
from textual.widget import Widget
from textual import on
from textual.widgets import Button
from textual.containers import  Vertical

from src.ui.widgets.form_config_enigma.view_config_rotor import ViewConfigRotor
from src.ui.widgets.form_config_enigma.event_changes_in_config import EventChangesInConfig
from src.ui.widgets.form_config_enigma.event_delet_config_rotor import EventDeletConfigRotor




class ContainerConfigRotor(Widget):
    DEFAULT_CSS = '''
    ContainerConfigRotor Vertical.container-config{
        min-height: 0;
        max-height: 16;
        width: 110;
        overflow-y: auto;
    }
    ContainerConfigRotor{
        min-height: 3;
        max-height: 20;
        width: 110;
        margin: 1 0;
    }
    
    ContainerConfigRotor Button#add-rotor{
        width: 110;
        text-align: center;
    }
    '''
    
    def __init__(self) -> None:
        super().__init__()
        
        self.__list_config: list[ViewConfigRotor] = []
        self.__container_rotors = Vertical(classes="container-config")
        self.__button_add_rotor = Button("Add Rotor", id= "add-rotor", compact=True)
    
    
    @property
    def list_view_config(self)  -> list[ViewConfigRotor]:
        return self.__list_config
    
    
    def compose(self) -> Generator[Widget, None, None]:
        yield self.__button_add_rotor
        yield self.__container_rotors
    
    
    @on(Button.Pressed, "#add-rotor")
    async def add_rotor(self) -> None:
        view_config = ViewConfigRotor(len(self.__list_config) + 1, self)
        self.__list_config.append(view_config)
        await self.__container_rotors.mount(view_config)
        self.refresh()
        self.post_message(EventChangesInConfig())
    
    
    def on_event_delet_config_rotor(self, event: EventDeletConfigRotor) -> None:
        config: ViewConfigRotor = self.__list_config.pop(event.index - 1)
        self.__container_rotors.remove_children([config])
        self.__update_titles_of_config()
        self.refresh()
    
    
    def __update_titles_of_config(self) -> None:
        for index, config in enumerate(iterable=self.__list_config):
            config.update_title_rotor(index + 1)
