from typing import Generator
import pyperclip

from textual.app import App
from textual import on
from textual.widgets import Input, Header, Button
from textual.widget import Widget
from textual.containers import Horizontal, Vertical

from src.core.enigma import Enigma
from src.core.config import ConfigEnigma, DictDinamicConfig

from src.ui.widgets import ViewConfigEnigma, ViewDataEnigma
from src.ui.events import EventReEncript



class SimulatorEnigmaApp(App[None]):
    CSS_PATH = "style.tcss"
    DEFAULT_CSS = '''
    
    SimulatorEnigmaApp Horizontal.main-content{
        align-horizontal: center;
    }
    
    SimulatorEnigmaApp Vertical.main-content{
        max-width: 250;
    }
    
    SimulatorEnigmaApp Header.title{
        margin-bottom: 2;
        height: 3;
    }

    SimulatorEnigmaApp Button.copy{
        margin-left: 5;
        margin-top: 1;
    }
    '''
    
    def __init__(self, enigma: Enigma) -> None:
        super().__init__()
        
        self.enigma: Enigma = enigma
        self.titulo = Header(name="Enigma Machine", classes="title")
        self.input = Input(id= "input", placeholder="input")
        self.output = Input(id = "output", disabled=True, placeholder= "output")
        self.view_data_enigma = ViewDataEnigma()
        self.view_config_enigma = ViewConfigEnigma()
    
    
    def compose(self) -> Generator[Widget, None, None]:
        with Vertical(classes="main-content"):
            yield self.titulo
            yield self.input
            yield self.output
            yield Button("Copy Output", id="copy")
            
            with Horizontal(classes="main-content"):
                yield self.view_data_enigma
                yield self.view_config_enigma
    
    
    def on_input_changed(self, event: Input.Changed) -> None:
        self.enigma.reset()
        
        self.input.value = self.input.value.upper()
        input: str = self.input.value
        output: str = self.enigma.encryption_text(input)
        self.output.value = output
        
        self.update_view_data_enigma()
    
    
    def on_event_re_encript(self, event: EventReEncript) -> None:
        config: ConfigEnigma[DictDinamicConfig] = ConfigEnigma(event.config)
        self.enigma.apply_dinamic_config(config)
        
        input: str = self.input.value
        output: str = self.enigma.encryption_text(input)
        self.output.value = output
        
        self.update_view_data_enigma()
    
    
    def update_view_data_enigma(self) -> None:
        self.view_data_enigma.update(
            info_models= " - ".join([model for model in self.enigma.models_rotors]),
            info_positon= " - ".join([data for data in self.enigma.position_rotors]),
            info_rings= " - ".join([data for data in self.enigma.rings_rotors]),
            info_reflect= self.enigma.model_reflect,
            info_interchanger= self.enigma.config_interchanger
        )
    
    
    @on(Button.Pressed, "#copy")
    def copy_output(self) -> None:
        
        pyperclip.copy(self.output.value)
