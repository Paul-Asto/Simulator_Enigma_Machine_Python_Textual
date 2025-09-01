from typing import Self, TYPE_CHECKING
from src.core.types import LetterAbc, ModelRotor
from src.core.utilities import (
    validate_index_letter_enigm,
    from_letter_to_index,
    from_index_to_letter,
)

if TYPE_CHECKING:
    from src.core.config import DictConfigRotor



class Rotor:
    
    def __init__(self, model: ModelRotor, cabling: str, notch: LetterAbc, position_initial: LetterAbc = "A", position_ring: LetterAbc = "A") -> None:
        self.validate_cabling(cabling)
        
        self.__model: ModelRotor = model
        self.__cabling: str = cabling.upper() 
        self.__len_cabling: int = len(cabling)
        self.__index_position: int = from_letter_to_index(position_initial)
        self.__index_ring: int = from_letter_to_index(position_ring)
        self.__index_notch: int = from_letter_to_index(notch)
        
        self.__data_encription: dict[int, int] = {
            index: from_letter_to_index( letter)
            for index, letter in enumerate(self.__cabling)
        }
        
        self.__data_decript: dict[int, int] = {
            value: key
            for key, value in self.__data_encription.items()
        }
    
    
    def __str__(self) -> str:
        result: str = f"Rotor: {self.model} \n"
        result += f"Cabling:  {self.cabling}\n"
        result += f"Position: {self.position_letter}\n"
        result += f"Notch:    {self.notch_letter}\n"
        result += f"Ring:     {self.ring_letter}"
        
        return result
    
    
    @property
    def config_data(self) -> "DictConfigRotor":
        return {
            "position": self.position_letter,
            "ring": self.ring_letter,
            "model": self.model,
        }
    
    
    @property
    def real_index_position(self) -> int:
        return self.__calculate_index_in_cycle(self.__index_position - self.__index_ring)
    
    
    @property
    def cabling(self) -> str:
        return self.__cabling
    
    
    @property
    def model(self) -> ModelRotor:
        return self.__model
    
    
    @property
    def position_letter(self) -> LetterAbc:
        return from_index_to_letter(self.__index_position)
    
    
    @property
    def ring_letter(self) -> LetterAbc:
        return from_index_to_letter(self.__index_ring)
    
    
    @property
    def notch_letter(self) -> LetterAbc:
        return from_index_to_letter(self.__index_notch + self.__index_ring)
    
    
    @property
    def in_notch_position(self) -> bool:
        return self.real_index_position == self.__index_notch
    
    
    def __calculate_index_in_cycle(self, index: int) -> int:
            return \
                index % self.__len_cabling \
                if index >= 0 else \
                self.__len_cabling - (abs(index) % self.__len_cabling)
    
    
    def validate_cabling(self, cabling: str) -> None:
        #Not Implemented
        pass
    
    
    def rotate(self, value: int) -> None:
        new_index: int = self.__calculate_index_in_cycle(self.__index_position + value)
        self.__index_position = new_index
    
    
    def modify_position(self, letter: LetterAbc)  -> Self:
        self.__index_position = from_letter_to_index(letter)
        return self
    
    
    def modify_ring(self, letter: LetterAbc)  -> Self:
        self.__index_ring = from_letter_to_index(letter)
        return self
    
    
    def encryption_index_letter(self, index: int) -> int:
        validate_index_letter_enigm(index)
        
        start_index: int = self.__calculate_index_in_cycle(index + self.real_index_position)
        encrypt_index: int = self.__data_encription[start_index]
        end_index: int = self.__calculate_index_in_cycle(encrypt_index - self.real_index_position)
        return end_index
    
    
    def encryption_letter(self, letter: LetterAbc) -> LetterAbc:
        index = from_letter_to_index(letter)
        
        start_index: int = self.__calculate_index_in_cycle(index + self.real_index_position)
        encrypt_index: int = self.__data_encription[start_index]
        end_index: int = self.__calculate_index_in_cycle(encrypt_index - self.real_index_position)
        return from_index_to_letter(end_index)
    
    
    def decrypt_index_letter(self, index: int) -> int:
        validate_index_letter_enigm(index)
        
        start_index: int = self.__calculate_index_in_cycle(index + self.real_index_position)
        encrypt_index: int = self.__data_decript[start_index]
        end_index: int = self.__calculate_index_in_cycle(encrypt_index - self.real_index_position)
        return end_index
    
    
    def decrypt_letter(self, letter: LetterAbc) -> LetterAbc:
        index: int = from_letter_to_index(letter)
        
        start_index: int = self.__calculate_index_in_cycle(index + self.real_index_position)
        encrypt_index: int = self.__data_decript[start_index]
        end_index: int = self.__calculate_index_in_cycle(encrypt_index - self.real_index_position)
        return from_index_to_letter(end_index)