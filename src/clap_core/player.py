from clap_core.hands import Hand

class Player:
    
    def __init__(self) -> None:
        self.qi = 0
        self.shield = 0
    
    def canPlay(self, hand: Hand):
        return False
