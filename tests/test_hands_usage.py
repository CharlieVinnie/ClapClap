from clap_core.hands import HANDS
from clap_core.player import Player

class TestHandsUsing:

    def check_hand_can_be_used(self, qi: int, shield: int, hand_name: str):
        hand = HANDS[hand_name]
        player = Player()
        player.qi = qi
        player.shield = shield
        return player.canPlay(hand)

    def test_can_use_hands(self):
        
        assert self.check_hand_can_be_used(qi=0, shield=0, hand_name="气")