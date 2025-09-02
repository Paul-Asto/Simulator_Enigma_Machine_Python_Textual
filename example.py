

# Ejemplo de encriptacion simple
from src.core.enigma import Enigma

enigma = Enigma()

input_text = "EJEMPLO DE TEXTO ENCRIPTADO"
output_text: str = enigma.encryption_text(input_text)

print(output_text)    #Output: ZBMDWTP GP YJWLC NYLZPQLITT



#Configuracion opcional inicial del enigma
from src.core.enigma import Enigma
from src.core.config import ConfigEnigma, DictRequiredConfig, DictDinamicConfig

config = ConfigEnigma[DictRequiredConfig]({
    "rotors": [
        {"model": "III", "position": "C"},
        {"model": "IV"},
        {"model": "VII", "position": "I", "ring": "N"}
    ],
    "reflect": "III",
    "interchanger": [
        {"letter_a": "E", "letter_b": "L"},
        {"letter_a": "M", "letter_b": "X"},
        {"letter_a": "G", "letter_b": "I"}
    ]
})

# Configuracion al inicio de la creacion de la instancia
enigma = Enigma(config)

# Configuracion posterior
enigma.apply_required_config(config)

# Modificacion de la configuracion simple
enigma.apply_dinamic_config(ConfigEnigma[DictDinamicConfig]({
    "reflect": "IV"
}))

enigma.apply_dinamic_config(ConfigEnigma[DictDinamicConfig]({
    "interchanger": [{"letter_a": "C", "letter_b": "L"}]
}))

# Reset a la configuracion inicial
enigma.reset()

# Setea la configuracion actual como la configuracion inicial, al momento de resetear usara esta configuracion como inicio
enigma.save_current_config()

# Configurar posicion de rotores
enigma.config_position_rotors("ABC")

# Configurar anillos de rotores
enigma.config_rings_rotors("AAA")

#Configurar las conexiones de intercambio
enigma.apply_config_interchanger([
    {"letter_a": "M", "letter_b": "W"},
    {"letter_a": "R", "letter_b": "I"}
])


# Informacion
enigma = Enigma()

print(enigma.position_rotors)        # example: AAA
print(enigma.models_rotors)          # example: ("I", "IV", "II")
print(enigma.config_interchanger)    # example: AC TY OK NF
print(enigma.model_reflect)          # example: III

print(enigma.current_config)        
''' EXAMPLE 
{
    "rotors": [
        {"model": "III", "position": "C"},
        {"model": "IV"},
        {"model": "VII", "ring": "N"}
    ],
    "reflect": "III",
    "interchanger": [
        {"letter_a": "E", "letter_b": "L"},
        {"letter_a": "M", "letter_b": "X"},
    ]
}'''
