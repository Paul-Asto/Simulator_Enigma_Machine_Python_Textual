
from typing import TypedDict, Optional, Generic, TypeVar, NotRequired
from src.core.types import  ModelReflect, ModelRotor, LetterAbc



class DictConfigRotor(TypedDict):
    model: ModelRotor
    position: NotRequired[LetterAbc]
    ring: NotRequired[LetterAbc]



class DictConfigInterchanger(TypedDict):
    letter_a: LetterAbc
    letter_b: LetterAbc




class DictDinamicConfig(TypedDict):
    rotors: NotRequired[list[DictConfigRotor]]
    reflect: NotRequired[ModelReflect] 
    interchanger: NotRequired[list[DictConfigInterchanger]]



class DictRequiredConfig(TypedDict):
    rotors: list[DictConfigRotor]
    reflect: ModelReflect 
    interchanger: NotRequired[list[DictConfigInterchanger]] 



T = TypeVar('T', DictDinamicConfig, DictRequiredConfig)

class ConfigEnigma(Generic[T]):
    def __init__(self, data_config: T) -> None:
        self.__data: T = data_config
        self.validate_data()
    
    
    def validate_data(self) -> None:
        # Not Implemented
        pass
    
    
    @property
    def models_rotors(self) -> tuple[ModelRotor, ...]:
        return tuple([config.get("model") for config in self.required_config_rotors])
    
    
    @property
    def required_config_rotors(self)  -> list[DictConfigRotor]:
        config_rotors: Optional[list[DictConfigRotor]] = self.__data.get("rotors")
        
        if config_rotors is None:
            raise Exception(f"La configuracion actual no cuenta con rotores {config_rotors}")
        
        return config_rotors
    
    
    @property
    def optional_config_rotors(self) -> Optional[list[DictConfigRotor]]:
        return self.__data.get("rotors")
        
    
    
    @property
    def required_config_reflect(self) -> ModelReflect:
        config_reflect: Optional[ModelReflect] = self.__data.get("reflect")
        
        if config_reflect is None:
            raise Exception(f"La configuracion Actual no cuenta con reflector: {config_reflect}")
        
        return config_reflect
    
    
    @property
    def optional_config_reflect(self) -> Optional[ModelReflect]:
        return self.__data.get("reflect")
    
    
    @property
    def required_config_interchanger(self) -> list[DictConfigInterchanger]:
        return self.__data.get("interchanger", [])
    
    
    @property
    def optional_config_interchanger(self) -> Optional[list[DictConfigInterchanger]]:
        return self.__data.get("interchanger")
    
    
    @property
    def required_data(self) -> DictRequiredConfig:
        return {
            "rotors": self.required_config_rotors,
            "reflect": self.required_config_reflect,
            "interchanger": self.required_config_interchanger
        }
    
    
    @property
    def optional_data(self) -> DictDinamicConfig:
        result: DictDinamicConfig = {}
        
        if not self.optional_config_rotors is None:
            result["rotors"] = self.optional_config_rotors
        
        if not self.optional_config_reflect is None:
            result["reflect"] = self.optional_config_reflect
        
        if not self.optional_config_interchanger is None:
            result["interchanger"] = self.optional_config_interchanger
        
        return result
    
    
    def to_required(self) -> "ConfigEnigma[DictRequiredConfig]":
        return ConfigEnigma(self.required_data)
    
    
    def to_dinamic(self)  -> "ConfigEnigma[DictDinamicConfig]":
        return ConfigEnigma(self.optional_data)
    
    
    def superimpose_config(self, config: "ConfigEnigma[DictDinamicConfig]") -> None:
        if not config.optional_config_rotors is None:
            self.__data["rotors"] = config.optional_config_rotors
        
        if not config.optional_config_reflect is None:
            self.__data["reflect"] = config.optional_config_reflect
        
        if not config.optional_config_interchanger is None:
            self.__data["interchanger"] = \
                config.optional_config_interchanger + self.optional_config_interchanger \
                if self.optional_config_interchanger != None else \
                config.optional_config_interchanger
    
    
    def set_data(self, data: DictRequiredConfig) -> None:
            self.__data["rotors"] = data["rotors"]
            self.__data["reflect"] = data["reflect"]
            self.__data["interchanger"] = data.get("interchanger", [])



DEFAULT_CONFIG: ConfigEnigma[DictRequiredConfig] = ConfigEnigma[DictRequiredConfig](
    {
        "rotors": 
        [
            {"model": "I", "position": "A"},
            {"model": "II", "position": "B"},
            {"model": "III", "position": "C"},
        ],
        
        "reflect": "I",
    }
)
