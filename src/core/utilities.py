from src.core.constants import ABC, SIZE_ABC
from src.core.types import LetterAbc



def validate_index_letter_enigm(index: int) -> None:
    if not (index >= 0 and index <SIZE_ABC):
        raise Exception(f"Indice de letra no valida: {index}")


def from_index_to_letter(index: int) -> LetterAbc:
    validate_index_letter_enigm(index)
    return ABC[index]


def from_letter_to_index(letter: LetterAbc) -> int:
    for i, l in enumerate(ABC):
        if letter == l:
            return i
        
    raise Exception(f"letra no valida en ABC soportado por enigma: {letter}")
