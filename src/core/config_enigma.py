
from typing import TypedDict, TYPE_CHECKING, Optional, Generic, TypeVar

from src.core.types import  (
    DictRequiredConfEnigm, 
    DictDinamicConfEnigm, 
    DictConfigRotor, 
    DictConfigInterchanger, 
    TypeReflect
)
from src.core.rotor import build_rotor
from src.core.reflect import build_reflect
from src.core.admin_interchangers import AdminInterChangers

if TYPE_CHECKING:
    from src.core.rotor import Rotor
    from src.core.reflect import Reflect


class DictBuildRequiredData(TypedDict):
    rotors: list["Rotor"]
    reflect: "Reflect"
    interchanger: AdminInterChangers


class DictBuildDinamicData(TypedDict):
    rotors: Optional[list["Rotor"]]
    reflect: Optional["Reflect"]
    interchanger: Optional[AdminInterChangers]



T = TypeVar('T', DictDinamicConfEnigm, DictRequiredConfEnigm)

class ConfigEnigma(Generic[T]):
    def __init__(self, data_config: T) -> None:
        self.data: T = data_config
        self.validate_data()
    
    def validate_data(self) -> None:
        # Not Implemented
        pass
    
    
    def build_validated_required_data(self) -> DictBuildRequiredData:
        rotors: list[DictConfigRotor] | None  = self.data.get("rotors")
        reflect: TypeReflect | None = self.data.get("reflect")
        interchanger: list[DictConfigInterchanger] | None = self.data.get("interchanger")
        
        if rotors is None:
            raise Exception(f"Error en el build estricto a falta de rotores {rotors}")
        
        if reflect is None:
            raise Exception(f"Error en el build estricto a falta del reflector: {reflect}")
        
        built_rotors: list["Rotor"] = [
            build_rotor(data_rotor.get("rotor"))
            .set_position( data_rotor.get("position", "A"))
            .set_ring(data_rotor.get("ring", "A"))
            for data_rotor in rotors
        ]
        
        built_reflect: "Reflect" = build_reflect(reflect)
        
        built_interchanger: AdminInterChangers = \
            AdminInterChangers(interchanger) \
            if not interchanger is None else \
            AdminInterChangers()
        
        return {
            "rotors" : built_rotors,
            "reflect": built_reflect,
            "interchanger": built_interchanger
        }
    
    
    def build_validated_dinamic_data(self) -> DictBuildDinamicData:
        rotors: list[DictConfigRotor] | None  = self.data.get("rotors")
        reflect: TypeReflect | None = self.data.get("reflect")
        interchanger: list[DictConfigInterchanger] | None = self.data.get("interchanger")
        
        built_rotors: list["Rotor"] | None = \
            None                    \
            if rotors is None else  \
            [
                build_rotor(data_rotor.get("rotor"))
                .set_position(data_rotor.get("position", "A"))
                .set_ring(data_rotor.get("ring", "A"))
                for data_rotor in rotors
            ] 
        
        built_reflect: Optional["Reflect"] = \
            None                    \
            if reflect is None else \
            build_reflect(reflect)
        
        
        built_interchanger: AdminInterChangers = \
            AdminInterChangers(interchanger) \
            if not interchanger is None else \
            AdminInterChangers()
        
        return {
            "rotors" : built_rotors,
            "reflect": built_reflect,
            "interchanger": built_interchanger
        }



DEFAULT_CONFIG: ConfigEnigma[DictRequiredConfEnigm] = ConfigEnigma[DictRequiredConfEnigm](
    {
        "rotors": 
        [
            {"rotor": "I", "position": "A"},
            {"rotor": "II", "position": "B"},
            {"rotor": "III", "position": "C"},
        ],
        
        "reflect": "III",
    }
)
