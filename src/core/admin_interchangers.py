from src.core.types import DictConfigInterchanger, AbcEnigma


class AdminInterChangers:
    
    def __init__(self, data_config: list[DictConfigInterchanger] = []) -> None:   
        self.exchange_data: dict[AbcEnigma, AbcEnigma] = {}
        
        for config in data_config:
            self.add_exchange_data(config)
    
    
    def __str__(self) -> str:
        return  "Interchanger: " + " ".join([ k + v for k, v in self.exchange_data.items()]) + "\n"
    
    
    def clear(self):
        self.exchange_data.clear()
    
    
    def validate_config(self, config: DictConfigInterchanger) -> None:
        # Not Implemented
        pass
    
    
    def exchange(self, letter: AbcEnigma) -> AbcEnigma:
        return self.exchange_data.get(letter, letter)
    
    
    def add_exchange_data(self, config: DictConfigInterchanger) -> None:
            self.validate_config(config)
            
            letter_a = config["letter_a"]
            letter_b = config["letter_b"]
            
            self.exchange_data[letter_a] = letter_b
            self.exchange_data[letter_b] = letter_a
