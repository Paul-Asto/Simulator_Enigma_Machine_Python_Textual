from typing import TYPE_CHECKING, Optional, cast
from src.core.types import DictDinamicConfEnigm, DictRequiredConfEnigm, AbcEnigma

from src.core.utilities import from_letter_to_index, from_index_to_letter
from src.core.config_enigma import ConfigEnigma, DEFAULT_CONFIG

if TYPE_CHECKING:
    from src.core.rotor import Rotor
    from src.core.reflect import Reflect
    from src.core.admin_interchangers import AdminInterChangers
    from src.core.config_enigma import DictBuildRequiredData, DictBuildDinamicData


class Enigma:
    
    def __init__(self, init_config: ConfigEnigma[DictRequiredConfEnigm] = DEFAULT_CONFIG) -> None:
        init_data_built: DictBuildRequiredData = init_config.build_validated_required_data()
        
        self.initial_config: "ConfigEnigma[DictDinamicConfEnigm]"= cast("ConfigEnigma[DictDinamicConfEnigm]", init_config)
        self.rotors: list["Rotor"] = init_data_built["rotors"]
        self.reflect: "Reflect" = init_data_built["reflect"]
        self.admin_intercharchers : "AdminInterChangers" = init_data_built["interchanger"]
        
        self.quantity_movs: int = 0
    
    
    def __str__(self) -> str:
        result: str = "Enigma Machine\n"
        result += "---------------\n"
        result += "Config Rotors: "
        result += "-".join(map(lambda rotor: rotor.name, self.rotors))            + " "
        result += "-".join(map(lambda rotor: rotor.position_letter, self.rotors)) + "\n"
        result += f"Reflect: {self.reflect.name}\n"
        result += str(self.admin_intercharchers)
        result += f"Numero de letras encriptadas {self.quantity_movs}"
        
        return result
    
    
    def reset(self) -> None:
        self.apply_config(self.initial_config)
    
    
    def apply_config(self, config: ConfigEnigma[DictDinamicConfEnigm]) -> None:
        config_data_built: DictBuildDinamicData = config.build_validated_dinamic_data()
        
        new_rotors: list["Rotor"] | None = config_data_built["rotors"]
        new_reflect: Optional["Reflect"] = config_data_built["reflect"] 
        new_interchanges: Optional["AdminInterChangers"] | None = config_data_built["interchanger"]
        
        if not new_rotors is None:
            self.rotors = new_rotors
        
        if not new_reflect is None:
            self.reflect = new_reflect
        
        if not new_interchanges is None:
            self.admin_intercharchers = new_interchanges
        
        self.initial_config = config
        self.quantity_movs = 0
    
    
    def mov_rotors(self) -> None:
        for rotor in self.rotors[::-1]:
            in_notch: bool = rotor.in_notch_position
            rotor.rotate(1)
            
            if not in_notch:
                break
    
    
    def encryption_text(self, text: str) -> str:
        list_input_real_letters: list[str] = [
            self.admin_intercharchers.exchange(letter)
            for letter in text.upper()
        ]
        
        list_input_index: list[int] = [
            -1                    \
            if letter == " " else \
            from_letter_to_index( letter)
            for letter in list_input_real_letters
        ]
        
        list_encript_index: list[int] = [
            -1
            if i == -1 \
            else self.process_encrypt(i)
            for i in list_input_index
        ]
        
        list_output_letters: list[str] = [
            " " \
            if i == -1 \
            else from_index_to_letter(i)
            for i in list_encript_index
        ]
        
        list_output_real_letters: list[str] = [
            self.admin_intercharchers.exchange( letter)
            for letter in list_output_letters
        ]
        
        return "".join(list_output_real_letters)
    
    
    def encryption_letter(self, letter: AbcEnigma) -> AbcEnigma:
        real_letter: AbcEnigma = self.admin_intercharchers.exchange(letter)
        input_index: int = from_letter_to_index(real_letter)
        encript_index: int = self.process_encrypt(input_index)
        output_letter: AbcEnigma = from_index_to_letter(encript_index)
        real_output_letter: AbcEnigma = self.admin_intercharchers.exchange(output_letter)
        
        return real_output_letter
    
    
    def process_encrypt(self, index: int) -> int:
        self.mov_rotors()
        
        for rotor in self.rotors[::-1]:
            index = rotor.encryption_index_letter(index)
        
        index = self.reflect.encryption_index_letter(index)
        
        for rotor in self.rotors:
            index = rotor.decrypt_index_letter(index)
        
        self.quantity_movs += 1
        
        return index
