from enum import Enum
from clap_core.hands import Hand

class GameStatus(Enum):
    ONGOING = 0
    FIRSTWIN = 1
    SECONDWIN = 2

class Judge:
    
    def __init__(self) -> None:
        pass

    def play(self, hand1: Hand, hand2: Hand):
        pass

    def gameStatus(self):
        pass