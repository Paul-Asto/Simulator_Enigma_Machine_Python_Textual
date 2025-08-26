from typing import Generator
from textual.app import App
from textual.widgets import Input, Static
from textual.widget import Widget

from src.core.enigma import Enigma
from src.core.types import DictDinamicConfEnigm
from src.core.config_enigma import ConfigEnigma

from src.ui.widgets import FormConfigEnigm
from src.ui.events import EventReEncript



class SimulatorEnigmaApp(App[None]):
    CSS_PATH = "style.tcss"
    
    def __init__(self, enigma: Enigma) -> None:
        super().__init__()
        
        self.enigma: Enigma = enigma
        self.titulo = Static("Enigma Machine", classes= "title")
        self.input = Input(id= "input", placeholder="Input")
        self.output = Input(id = "output", disabled=True, placeholder= "Output")
        self.view_config = Static(str(self.enigma))
    
    
    def compose(self) -> Generator[Widget, None, None]:
        yield self.titulo
        yield self.input
        yield self.output
        yield self.view_config
        yield FormConfigEnigm()
    
    
    def on_input_changed(self, event: Input.Changed) -> None:
        self.view_config.update(str(self.enigma))
        self.enigma.reset()
        
        self.input.value = self.input.value.upper()
        input: str = self.input.value
        output: str = self.enigma.encryption_text(input)
        self.output.value = output
    
    
    def on_event_re_encript(self, event: EventReEncript) -> None:
        config: ConfigEnigma[DictDinamicConfEnigm] = ConfigEnigma(event.config)
        
        self.enigma.apply_config(config)
        self.view_config.update(str(self.enigma))
        
        input: str = self.input.value
        output: str = self.enigma.encryption_text(input)
        self.output.value = output
