from typing import Generator

from textual.widget import Widget
from textual.widgets import Static
from textual.containers import Vertical

from src.ui.widgets.view_data_enigma.view_info import ViewInfo



class ViewDataEnigma(Widget):
    DEFAULT_CSS = '''
    ViewDataEnigma{
    margin:1 3;
    align-horizontal: center;
    border:solid;
    width: 112;
    height: 32;
    }
    
    ViewDataEnigma Static.title{
    text-align: center;
    width: 90;
    }
    
    ViewDataEnigma Vertical.content{
    align-vertical: middle;
    width: 90;
    height: 29;
    }
    '''
    
    def __init__(self) -> None:
        super().__init__()
        
        self.__title                      = Static("CURRENT CONFIG ENIGMA", classes="title")
        self.__info_models_rotors         = ViewInfo("Models Rotors:")
        self.__info_position_rotors       = ViewInfo("Positions:")
        self.__info_position_rings       = ViewInfo("Rings:")
        self.__info_model_reflect         = ViewInfo("Model Reflect:")
        self.__info_config_interchanger   = ViewInfo("Config Interchanger:")
    
    
    def compose(self) -> Generator[Widget, None, None]:
        yield self.__title
        
        with Vertical(classes= "content"):
            yield self.__info_models_rotors        
            yield self.__info_position_rotors  
            yield self.__info_position_rings   
            yield self.__info_model_reflect        
            yield self.__info_config_interchanger  
    
    
    def update(self, info_models: str, info_positon: str, info_rings: str, info_reflect: str, info_interchanger: str) -> None:
        self.__info_models_rotors.update(info_models)
        self.__info_position_rotors.update(info_positon)
        self.__info_position_rings.update(info_rings)
        self.__info_model_reflect.update(info_reflect)
        self.__info_config_interchanger.update(info_interchanger)
