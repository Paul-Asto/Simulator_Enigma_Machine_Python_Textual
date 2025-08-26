from src.core.enigma import Enigma
from src.ui.app import SimulatorEnigmaApp


if __name__ == "__main__":
    enigm = Enigma()
    app = SimulatorEnigmaApp(enigm)
    app.run()
