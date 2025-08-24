from src.core.config_enigma import DEFAULT_CONFIG
from src.core.enigma import Enigma



enigm = Enigma(DEFAULT_CONFIG)
print(enigm)
print()

data_input = "ESTE ES UN EJEMPLO DE UN TEXTO ENCRIPTADO"
data_output: str = enigm.encryption_text(data_input)

print(data_input)
print(data_output)
print()
print(enigm)
