from typing import TYPE_CHECKING
from src.core.types import LetterAbc
from src.core.utilities import from_index_to_letter, from_letter_to_index

if TYPE_CHECKING:
    from src.core.config import DictConfigInterchanger



class InterChanger:
    
    def __init__(self, data_config: list["DictConfigInterchanger"] = []) -> None:   
        self.__exchange_data: dict[int, int] = {}
        self.apply_config(data_config)
    
    
    def __str__(self) -> str:
        return  "Interchanger: " + " ".join([conf.get("letter_a") + conf.get("letter_b") for conf in self.config_data]) + "\n"
    
    
    @property
    def config_data(self) -> list["DictConfigInterchanger"]:
        repeat_chars: list[int] = []
        result: list["DictConfigInterchanger"] =  []
        
        for key, value in  self.__exchange_data.items():
            if key in repeat_chars:
                continue
            
            result.append({
                "letter_a": from_index_to_letter(key),
                "letter_b": from_index_to_letter(value),
            })
            
            repeat_chars.append(value)
        
        return result
    
    
    def clear(self) -> None:
        self.__exchange_data.clear()
    
    
    def apply_config(self, data_config: list["DictConfigInterchanger"]) -> None:
        self.clear()
        
        for config in data_config:
            self.add_exchange_data(config)
    
    
    def validate_config(self, config: "DictConfigInterchanger") -> None:
        # Not Implemented
        pass
    
    
    def exchange_letter(self, letter: LetterAbc) -> LetterAbc:
        index: int = from_letter_to_index(letter)
        exchange_index: int | None = self.__exchange_data.get(index)
        return from_index_to_letter(exchange_index) if exchange_index != None else letter
    
    
    def exchange_index(self, index: int) -> int:
        return self.__exchange_data.get(index, index)
    
    
    def add_exchange_data(self, config: "DictConfigInterchanger") -> None:
            self.validate_config(config)
            
            letter_a: int = from_letter_to_index(config["letter_a"])
            letter_b: int = from_letter_to_index(config["letter_b"])
            
            self.__exchange_data[letter_a] = letter_b
            self.__exchange_data[letter_b] = letter_a
