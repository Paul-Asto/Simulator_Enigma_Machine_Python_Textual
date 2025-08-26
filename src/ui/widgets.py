from typing import Generator, cast
from textual.widget import Widget
from textual import on
from textual.widgets import Static, Select, Button
from textual.containers import Horizontal, Vertical

from src.core.utilities import from_index_to_letter
from src.core.constants import SIZE_ABC, ABC
from src.core.types import DictConfigRotor, DictConfigInterchanger

from src.ui.events import EventDeletConfigRotor, EventChangesInConfig, EventReEncript



class ViewSelect(Widget):
    DEFAULT_CSS = '''
    ViewSelect{
        width: 30;
        height: 4;
        border: solid;
    }
    ViewSelect Static.title{
        text-align: center;
    }
    
    ViewSelect Select Static{
        text-align: center;
    }
    '''
    
    def __init__(self, title: str, classes: str = "", content: list[str] = []) -> None:
        super().__init__(classes= classes)
        
        self.title = Static(title, classes="title")
        self.select: Select[str] = Select([
            (d, d) for d in content
        ], allow_blank= False, compact= True)
    
    
    def compose(self) -> Generator[Widget, None, None]:
        with Vertical():
            yield self.title
            yield self.select
    
    
    @on(Select.Changed)
    def on_select_changed(self, event: Select.Changed) -> None:
        self.post_message(EventChangesInConfig())



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
    
    SelectAbc Horizontal{
        align-horizontal: center;
    }
    
    '''
    
    def __init__(self, title: str, index: int = 0) -> None:
        super().__init__()
        
        self.index: int = index
        self.title = Static(title, classes= "title")
        self.button_minos = Button("-", classes="minus", compact= True)
        self.data = Static(f"{self.index + 1} {from_index_to_letter(self.index)}", classes="data-abc")
        self.button_plus = Button("+", classes="plus", compact= True)
    
    
    def compose(self) -> Generator[Widget, None, None]:
        yield self.title
        with Horizontal():
            yield self.button_minos
            yield self.data
            yield self.button_plus
    
    
    @on(Button.Pressed, ".plus")
    def plus(self) -> None:
        new_index: int = self.index + 1
        self.index = new_index % SIZE_ABC 
        self.__update_data()
        self.post_message(EventChangesInConfig())
    
    
    @on(Button.Pressed, ".minus")
    def minus(self) -> None:
        new_index: int = self.index - 1
        self.index = new_index \
            if new_index >= 0 else \
            SIZE_ABC - (abs(new_index) % SIZE_ABC)
        self.__update_data()
        self.post_message(EventChangesInConfig())
        
    def __update_data(self):
        self.data.update(f"{self.index + 1} {from_index_to_letter(self.index)}")



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
        
        self.index: int = id
        self.select_type = ViewSelect(f"Rotor {id}", content=["I", "II", "III", "IIII", "V"])
        self.select_position = SelectAbc("Posicion")
        self.select_ring = SelectAbc("Ring")
        self.delete_button = Button("Delete", classes="delete")
    
    
    def compose(self) -> Generator[Widget, None, None]:
        with Horizontal(classes="content"):
            yield self.select_type
            yield self.select_position
            yield self.select_ring
            yield self.delete_button
    
    
    @on(Button.Pressed, ".delete")
    def delete_rotor(self) -> None:
        self.post_message(EventDeletConfigRotor(self.index))
        self.post_message(EventChangesInConfig())
    
    
    def update_title_rotor(self, id:int) -> None:
        self.index = id
        self.select_type.title.update(f"Rotor {id}")



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
        
        self.list_config: list[ViewConfigRotor] = []
        self.container_rotors = Vertical(classes="container-config")
        self.button_add_rotor = Button("Add Rotor", id= "add-rotor", compact=True)
    
    
    def compose(self) -> Generator[Widget, None, None]:
        yield self.button_add_rotor
        yield self.container_rotors
    
    
    @on(Button.Pressed, "#add-rotor")
    async def add_rotor(self) -> None:
        view_config = ViewConfigRotor(len(self.list_config) + 1, self)
        self.list_config.append(view_config)
        await self.container_rotors.mount(view_config)
        self.refresh()
        self.post_message(EventChangesInConfig())
    
    
    def on_event_delet_config_rotor(self, event: EventDeletConfigRotor) -> None:
        config: ViewConfigRotor = self.list_config.pop(event.index - 1)
        self.container_rotors.remove_children([config])
        self.__update_titles_of_config()
        self.refresh()
    
    
    def __update_titles_of_config(self) -> None:
        for index, config in enumerate(iterable=self.list_config):
            config.update_title_rotor(index + 1)



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
    
    ViewConfigInterchanges Horizontal Select{
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
        
        self.title = Static("Interchangers", classes="title")
        self.list_chars: list[str] = list(ABC)
        self.data = Static(classes="data")
        
        self.select_a: Select[str] = Select([
            (char, char)
            for char in self.list_chars
        ], compact=True, allow_blank=False)
        
        self.select_b: Select[str] = Select([
            (char, char)
            for char in self.list_chars
        ], compact=True, allow_blank= False)
        
        self.button_add = Button("Add", id="add", compact= True)
        self.button_clear = Button("Clear", id="clear", compact= True)
    
    
    @property
    def data_interchangers(self) -> list[tuple[str, str]]:
        data: str = str(self.data.render())
        if data == "": return []
        return [(d[0], d[1])for d in data.strip().split(" ")]
    
    
    def compose(self) -> Generator[Widget, None, None]:
        with Vertical(classes="content"):
            yield self.title
            
            with Horizontal(classes="content"):
                yield self.data
                yield self.select_a
                yield self.select_b
                yield self.button_add
                yield self.button_clear
    
    
    @on(Button.Pressed, "#add")
    def add_interchanger(self) -> None:
        value_a: str = cast(str, self.select_a.value)
        value_b: str = cast(str, self.select_b.value)
        
        if value_a == value_b:
            return
        
        data = self.data.render()
        self.data.update(f"{data} {value_a}{value_b}")
        
        self.list_chars.remove(value_a)
        self.list_chars.remove(value_b)
        
        self.update_options(self.list_chars)
        self.post_message(EventChangesInConfig())
    
    
    @on(Button.Pressed, "#clear")
    def clear_interchangers(self) -> None:
        self.data.update()
        self.list_chars = list(ABC)
        self.update_options(self.list_chars)
        self.post_message(EventChangesInConfig())
    
    
    def update_options(self, options: list[str]) -> None:
        self.select_a.set_options([
            (char, char)
            for char in options
        ])
        
        self.select_b.set_options([
            (char, char)
            for char in options
        ])



class FormConfigEnigm(Widget):
    DEFAULT_CSS = '''
    FormConfigEnigm{
    border: solid;
    width: 112;
    height: 32;
    }

    FormConfigEnigm Static.title{
        text-align: center;
    }



    '''
    
    def __init__(self) -> None:
        super().__init__()
        
        self.title = Static("CONFIGURACION DEL ENIGMA", classes="title")
        self.config_interchangers = ViewConfigInterchanges()
        self.reflect_select = ViewSelect("Reflect", content=["I", "II", "III"])
        self.container_config_rotor = ContainerConfigRotor()
    
    
    def compose(self) -> Generator[Widget, None, None]:
        with Vertical():
            yield self.title
            yield self.config_interchangers
            yield self.reflect_select
            yield self.container_config_rotor
    
    
    def on_event_changes_in_config(self, event: EventChangesInConfig) -> None:
        rotors: list[DictConfigRotor] =  [
            {
            "rotor": cast(str, config.select_type.select.value),
            "position": from_index_to_letter(config.select_position.index),
            "ring": from_index_to_letter(config.select_ring.index),
            }
            for config in self.container_config_rotor.list_config
        ]
        
        reflect: str = cast(str, self.reflect_select.select.value)
        
        interchangers: list[DictConfigInterchanger] = [
            {"letter_a": a, "letter_b": b} 
            for a, b in self.config_interchangers.data_interchangers
        ]
        
        self.post_message(EventReEncript({
            "rotors":  rotors,
            "reflect": reflect,
            "interchanger": interchangers
        }))
