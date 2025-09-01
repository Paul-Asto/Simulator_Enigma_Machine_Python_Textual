from typing import TYPE_CHECKING, TypedDict, Optional
from src.core.types import ModelReflect, ModelRotor, LetterAbc

from src.core.rotor import Rotor
from src.core.reflect import Reflect
from src.core.interchangers import InterChanger

if TYPE_CHECKING:  
    from src.core.config import (
        DictConfigRotor, 
        DictConfigInterchanger, 
        DictDinamicConfig, 
        DictRequiredConfig
    )


class DictBuildRequiredData(TypedDict):
    rotors: list["Rotor"]
    reflect: "Reflect"
    interchanger: InterChanger


class DictBuildDinamicData(TypedDict):
    rotors: Optional[list["Rotor"]]
    reflect: Optional["Reflect"]
    interchanger: Optional[InterChanger]


class BuilderEnigma:
    
    @classmethod
    def build_rotor_by_model(cls, model: ModelRotor) -> Rotor:
        match(model):
            case "I":    return Rotor(model= "I", cabling= "EKMFLGDQVZNTOWYHXUSPAIBRCJ", notch= "Q")
            
            case "II":   return Rotor(model= "II", cabling= "AJDKSIRUXBLHWTMCQGZNPYFVOE", notch= "E")
            
            case "III":  return Rotor(model= "III", cabling= "BDFHJLCPRTXVZNYEIWGAKMUSQO", notch= "V")
            
            case "IV":   return Rotor(model= "IV", cabling= "ESOVPZJAYQUIRHXLNFTGKDCMWB", notch= "J")
            
            case "V":    return Rotor(model= "V", cabling= "VZBRGITYUPSDNHLXAWMJQOFECK", notch= "Z")
            
            case "VI":   return Rotor(model= "VI", cabling= "JPGVOUMFYQBENHZRDKASXLICTW", notch= "Z")
            
            case "VII":  return Rotor(model= "VII", cabling= "NZJHGRCXMYSWBOUFAIVLPEKQDT", notch= "Z")
            
            case "VIII": return Rotor(model= "VIII", cabling= "FKQHTLXOCBJSPDZRAMEWNIUYGV", notch= "Z")
            
            case _:  
                raise Exception(f"Error en el build del rotor: {model} no existente")
    
    
    @classmethod
    def build_rotor_by_config(cls, config: "DictConfigRotor") -> Rotor:
        model: ModelRotor           = config.get("model")
        position_letter:LetterAbc   = config.get("position", "A")
        ring_letter:LetterAbc       = config.get("ring", "A")
        
        return cls.build_rotor_by_model(model)      \
                .modify_position(position_letter)  \
                .modify_ring(ring_letter)          \
    
    
    @classmethod
    def build_rotors_by_config(cls, configs: list["DictConfigRotor"]) -> list[Rotor]:
        return [cls.build_rotor_by_config(config) for config in configs]
    
    
    @classmethod
    def build_reflect_by_model(cls, model: ModelReflect) -> Reflect:
        match(model):
            case "I":   return Reflect(model= "I", cabling= "ENKQAUYWJICOPBLMDXZVFTHRGS")
            
            case "II":  return Reflect(model= "II", cabling= "RDOBJNTKXEHVPFCMZAWGYLSIUQ")
            
            case "III": return Reflect(model= "III", cabling= "YRUHQSLDPXNGOKMIEBFZCWVJAT")
            
            case "IV":  return  Reflect(model= "IV", cabling= "RDOBJNTKVEHMLFCWZAXGYIPSUQ")
            
            case "V":   return Reflect(model= "V", cabling= "FVPJIAOYEDRZXWGCTKUQSBNMHL")
            
            case _:
                raise Exception(f"Error en el build del relector: {model}")
    
    
    @classmethod
    def build_interchanger_by_config(cls, configs: list["DictConfigInterchanger"]) -> InterChanger:
        return InterChanger(configs)
    
    
    @classmethod
    def build_required_data(cls, config: "DictRequiredConfig") -> DictBuildRequiredData:
        config_rotors: list["DictConfigRotor"] = config.get("rotors")
        config_reflect: ModelReflect = config.get("reflect")
        config_interchanger: list["DictConfigInterchanger"] = config.get("interchanger", [])
        
        return {
            "rotors": cls.build_rotors_by_config(config_rotors),
            "reflect": cls.build_reflect_by_model(config_reflect),
            "interchanger": cls.build_interchanger_by_config(config_interchanger)
        }
    
    
    @classmethod
    def build_dinamic_data(cls, config: "DictDinamicConfig") -> DictBuildDinamicData:
        config_rotors: Optional[list["DictConfigRotor"]] = config.get("rotors")
        config_reflect: Optional[ModelReflect] = config.get("reflect")
        config_interchanger: Optional[list["DictConfigInterchanger"]] = config.get("interchanger")
        
        built_rotors: Optional[list["Rotor"]] = \
            None                    \
            if config_rotors is None else  \
            cls.build_rotors_by_config(config_rotors)
        
        built_reflect: Optional["Reflect"] = \
            None                    \
            if config_reflect is None else \
                cls.build_reflect_by_model(config_reflect)
        
        built_interchanger: Optional[InterChanger] = \
            None \
            if config_interchanger is None else \
            cls.build_interchanger_by_config(config_interchanger)
        
        return {
            "rotors": built_rotors,
            "reflect": built_reflect,
            "interchanger": built_interchanger,
        }
