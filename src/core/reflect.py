from src.core.utilities import from_letter_to_index, validate_index_letter_enigm, from_index_to_letter
from src.core.types import  ModelReflect, LetterAbc



class Reflect:
    
    def __init__(self, model: ModelReflect, cabling: str) -> None:
        self.validate_cabling(cabling)
        
        self.__model: ModelReflect = model
        self.__cabling: str = cabling.upper()
        self.__data_encription: dict[int, int] = {
            index: from_letter_to_index( letter)
            for index, letter in enumerate(self.cabling)
        }
    
    
    def __str__(self) -> str:
        result: str = f"Reflect: {self.model}\n"
        result += f"Cabling: {self.cabling}\n"
        
        return result
    
    
    def validate_cabling(self, cabling: str) -> None:
        # Not Implemented
        pass
    
    
    @property
    def model(self) -> ModelReflect:
        return self.__model
    
    
    @property
    def cabling(self) -> str:
        return self.__cabling
    
    
    def encryption_index_letter(self, index: int) -> int:
        validate_index_letter_enigm(index)
        
        return self.__data_encription[index]
    
    
    def encryption_letter(self, letter: LetterAbc) -> LetterAbc:
        index: int = from_letter_to_index(letter)
        encript_index: int =  self.__data_encription[index]

        return from_index_to_letter(encript_index)
