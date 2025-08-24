from typing import Literal, TypedDict, NotRequired

TypeRotor = Literal["I", "II", "III", "IIII", "V"]
TypeReflect = Literal["I", "II", "III", "IIII"]

AbcEnigma = Literal[
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]



class DictConfigRotor(TypedDict):
    rotor: TypeRotor
    position: NotRequired[AbcEnigma]
    ring: NotRequired[AbcEnigma]


class DictConfigInterchanger(TypedDict):
    letter_a: AbcEnigma
    letter_b: AbcEnigma



class DictDinamicConfEnigm(TypedDict):
    rotors: NotRequired[list[DictConfigRotor]]
    reflect: NotRequired[TypeReflect] 
    interchanger: NotRequired[list[DictConfigInterchanger]]


class DictRequiredConfEnigm(TypedDict):
    rotors: list[DictConfigRotor]
    reflect: TypeReflect 
    interchanger: NotRequired[list[DictConfigInterchanger]] 
