from enum import Enum
from clap_core.player import Player

class GameStatus(Enum):
    ONGOING = 0
    FIRSTWIN = 1
    SECONDWIN = 2

class Judge:
    
    def __init__(self) -> None:
        self.player = ( Player(), Player() )

    def play(self, hand1: str, hand2: str):
        pass

    def gameStatus(self):
        return GameStatus.ONGOING