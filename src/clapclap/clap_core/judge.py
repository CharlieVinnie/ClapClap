from enum import Enum
from clapclap.clap_core.player import Player
from clapclap.clap_core.hands import kills

class ClapInternalError(Exception):
    pass

class GamePlayError(Exception):
    pass

class GameStatus(Enum):
    ONGOING = 0
    FIRSTWIN = 1
    SECONDWIN = 2

class Judge:
    
    def __init__(self) -> None:
        self.player = ( Player(), Player() )
        self.status = GameStatus.ONGOING

    def play(self, hand1: str, hand2: str):
        if self.status != GameStatus.ONGOING:
            raise GamePlayError("Game has already ended")
        
        self.player[0].play(hand1)
        self.player[1].play(hand2)

        first_win = kills(hand1,hand2)
        second_win = kills(hand2,hand1)

        if first_win and second_win:
            raise ClapInternalError("Mutual killing")
        elif first_win:
            self.status = GameStatus.FIRSTWIN
        elif second_win:
            self.status = GameStatus.SECONDWIN

    def gameStatus(self):
        return self.status