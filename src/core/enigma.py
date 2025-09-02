from typing import TYPE_CHECKING, Optional
from src.core.types import  LetterAbc, ModelReflect, ModelRotor

from src.core.utilities import from_letter_to_index, from_index_to_letter
from src.core.config import ConfigEnigma, DEFAULT_CONFIG
from src.core.builder import BuilderEnigma

if TYPE_CHECKING:
    from src.core.rotor import Rotor
    from src.core.reflect import Reflect
    from src.core.interchangers import InterChanger
    from src.core.builder import  DictBuildRequiredData
    from src.core.config import DictDinamicConfig, DictRequiredConfig, DictConfigInterchanger, DictConfigRotor



class Enigma:
    
    def __init__(self, config: ConfigEnigma["DictRequiredConfig"] = DEFAULT_CONFIG) -> None:
        init_data_built: DictBuildRequiredData = BuilderEnigma.build_required_data(config.required_data)
        
        self.__config: ConfigEnigma["DictRequiredConfig"] = config
        self.__rotors: list["Rotor"]                = init_data_built["rotors"]
        self.__reflect: "Reflect"                   = init_data_built["reflect"]
        self.__intercharcher : "InterChanger"       = init_data_built["interchanger"]
        
        self.save_current_config()
        self.__quantity_movs: int = 0
    
    
    def __str__(self) -> str:
        result: str = "Enigma Machine\n"
        result += "---------------\n"
        result += "Config Rotors: "
        result += "-".join(map(lambda rotor: rotor.model, self.__rotors))            + " "
        result += "-".join(map(lambda rotor: rotor.position_letter, self.__rotors)) + "\n"
        result += f"Reflect: {self.__reflect.model}\n"
        result += str(self.__intercharcher)
        result += f"Numero de letras encriptadas {self.__quantity_movs}"
        
        return result
    
    
    @property
    def n_movs(self) -> int:
        return self.__quantity_movs
    
    
    @property
    def n_rotors(self) -> int:
        return len(self.__rotors)
    
    
    @property
    def init_config(self)  -> "DictDinamicConfig":
        return self.__config.optional_data
    
    
    @property
    def current_config(self) -> "DictRequiredConfig":
        return {
            "rotors": [rotor.config_data for rotor in self.__rotors],
            "reflect": self.__reflect.model,
            "interchanger": self.__intercharcher.config_data
        }
    
    
    @property
    def model_reflect(self) -> ModelReflect:
        return self.__reflect.model
    
    
    @property
    def models_rotors(self) -> tuple[ModelRotor, ...]:
        return self.__config.models_rotors
    
    
    @property
    def position_rotors(self) -> str:
        return "".join([rotor.position_letter for rotor in self.__rotors])
    
    
    @property
    def rings_rotors(self) -> str:
        return "".join([rotor.ring_letter for rotor in self.__rotors])
    
    
    @property
    def config_interchanger(self) -> str:
        return " ".join([f"{config.get("letter_a")}{config.get("letter_b")}" for config in self.__intercharcher.config_data])
    
    
    def reset(self, config: ConfigEnigma["DictRequiredConfig"] | None = None) -> None:
        if config == None:
            self.apply_dinamic_config(self.__config.to_dinamic())
        
        else:
            self.apply_required_config(config)
    
    
    def save_current_config(self) -> None:
        self.__config.set_data(self.current_config)
        self.__quantity_movs = 0
    
    
    def config_position_rotors(self, config: str) -> None:
        if self.n_rotors != len(config):
            raise Exception(f"Error en el numero de configuraciones de posicion: rotores actuales {self.n_rotors} configuracion: {config}")
        
        for rotor, letter in zip(self.__rotors, config.upper()):
            rotor.modify_position(letter)
        
        self.save_current_config()
    
    
    def config_rings_rotors(self, config: str) -> None:
        if self.n_rotors != len(config):
            raise Exception(f"Error en el numero de configuraciones de ring: rotores actuales {self.n_rotors} configuracion: {config}")
        
        for rotor, letter in zip(self.__rotors, config.upper()):
            rotor.modify_ring(letter)
        
        self.save_current_config()
    
    
    def apply_config_interchanger(self, configs: list["DictConfigInterchanger"]) -> None:
        self.__intercharcher.apply_config(configs)
        
        self.save_current_config()
    
    
    def apply_dinamic_config(self, config: ConfigEnigma["DictDinamicConfig"]) -> None:
        config_rotors: Optional[list[DictConfigRotor]]                  = config.optional_config_rotors
        config_reflect: Optional[ModelReflect]                          = config.optional_config_reflect
        config_interchanger: Optional[list[DictConfigInterchanger]]     = config.optional_config_interchanger
        
        if not config_rotors is None:
            if self.models_rotors != config.models_rotors:
                self.__rotors = BuilderEnigma.build_rotors_by_config(config_rotors)
            
            else:
                for rotor, config_r in zip(self.__rotors, config_rotors):
                    new_position: LetterAbc | None = config_r.get("position")
                    new_ring: LetterAbc | None = config_r.get("ring")
                    
                    if new_position != None: rotor.modify_position(new_position)
                    if new_ring != None: rotor.modify_ring(new_ring)
        
        if not config_reflect is None and self.__reflect.model != config_reflect:
            self.__reflect = BuilderEnigma.build_reflect_by_model(config_reflect)
        
        if not config_interchanger is None:
            self.__intercharcher.apply_config(config_interchanger)
        
        self.save_current_config()
    
    
    def apply_required_config(self, config: ConfigEnigma["DictRequiredConfig"]) -> None:
        config_rotors: list[DictConfigRotor]                = config.required_config_rotors
        config_reflect: ModelReflect                        = config.required_config_reflect
        config_interchanger: list[DictConfigInterchanger]   = config.required_config_interchanger
        
        if self.models_rotors != config.models_rotors:
            self.__rotors = BuilderEnigma.build_rotors_by_config(config_rotors)
        
        else:
            for rotor, config_r in zip(self.__rotors, config_rotors):
                new_position: LetterAbc = config_r.get("position", "A")
                new_ring: LetterAbc = config_r.get("ring", "A")
                
                rotor.modify_position(new_position)
                rotor.modify_ring(new_ring)
        
        if self.__reflect.model != config_reflect:
            self.__reflect = BuilderEnigma.build_reflect_by_model(config_reflect)
        
        self.__intercharcher.apply_config(config_interchanger)
        self.save_current_config()
    
    
    def mov_rotors(self) -> None:
        for rotor in self.__rotors[::-1]:
            in_notch: bool = rotor.in_notch_position
            rotor.rotate(1)
            
            if not in_notch:
                break
    
    
    def encryption_text(self, text: str) -> str:    
        list_input_index: list[int] = [
            -1                    \
            if letter == " " else \
            from_letter_to_index( letter)
            for letter in text.upper()
        ]
        
        list_encript_index: list[int] = [
            -1
            if i == -1 \
            else self.__process_encrypt(i)
            for i in list_input_index
        ]
        
        list_output_letters: list[str] = [
            " " \
            if i == -1 \
            else from_index_to_letter(i)
            for i in list_encript_index
        ]
        
        return "".join(list_output_letters)
    
    
    def encryption_letter(self, letter: LetterAbc) -> LetterAbc:
        input_index: int = from_letter_to_index(letter)
        encript_index: int = self.__process_encrypt(input_index)
        output_letter: LetterAbc = from_index_to_letter(encript_index)
        
        return output_letter
    
    
    def __process_encrypt(self, index: int) -> int:
        self.mov_rotors()
        
        index = self.__intercharcher.exchange_index(index)
        
        for rotor in self.__rotors[::-1]:
            index = rotor.encryption_index_letter(index)
        
        index = self.__reflect.encryption_index_letter(index)
        
        for rotor in self.__rotors:
            index = rotor.decrypt_index_letter(index)
        
        index = self.__intercharcher.exchange_index(index)
        
        self.__quantity_movs += 1
        
        return index
