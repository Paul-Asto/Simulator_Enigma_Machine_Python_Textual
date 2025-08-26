from src.core.utilities import from_letter_to_index, validate_index_letter_enigm
from src.core.types import  TypeReflect



class Reflect:
    
    def __init__(self, name: TypeReflect, cabling: str) -> None:
        self.validate_cabling(cabling)
        
        self.__name: TypeReflect = name
        self.__cabling: str = cabling.upper()
        self.__data_encription: dict[int, int] = {
            index: from_letter_to_index( letter)
            for index, letter in enumerate(self.cabling)
        }
    
    
    def __str__(self) -> str:
        result: str = f"Reflect: {self.name}\n"
        result += f"Cabling: {self.cabling}\n"
        
        return result
    
    
    def validate_cabling(self, cabling: str) -> None:
        # Not Implemented
        pass
    
    
    @property
    def name(self) -> TypeReflect:
        return self.__name
    
    
    @property
    def cabling(self) -> str:
        return self.__cabling
    
    
    def encryption_index_letter(self, index: int) -> int:
        validate_index_letter_enigm(index)
        
        return self.__data_encription[index]



def build_reflect(name: TypeReflect) -> Reflect:
    if   name == "I":     return Reflect(name="I", cabling="ENKQAUYWJICOPBLMDXZVFTHRGS")
    elif name == "II":  return Reflect(name="II", cabling="RDOBJNTKXEHVPFCMZAWGYLSIUQ")
    elif name == "III": return Reflect(name="III", cabling="YRUHQSLDPXNGOKMIEBFZCWVJAT")
    
    raise Exception(f"Error en el build del relector: {name}")
