from clap_core.player import Player

class TestHandsUsing:

    def check_hand_can_be_used(self, hand: str, player_pre: Player):
        return player_pre.canPlay(hand)

    def test_can_use_hands(self):
        
        assert self.check_hand_can_be_used("气", Player())
        assert self.check_hand_can_be_used("盾", Player())

        assert self.check_hand_can_be_used("气", Player(qi=1, spark=2))

        assert self.check_hand_can_be_used("gi", Player(qi=1))
        assert not self.check_hand_can_be_used("gi", Player(shield=1))

        assert self.check_hand_can_be_used("破", Player(qi=2))
        assert not self.check_hand_can_be_used("破", Player(qi=1, shield=2))
        assert self.check_hand_can_be_used("黑洞", Player(qi=8))
        assert not self.check_hand_can_be_used("黑洞", Player(qi=6, shield=8))
        assert self.check_hand_can_be_used("小火", Player(shield=2))
        assert not self.check_hand_can_be_used("小火", Player(qi=2, shield=1))
        assert self.check_hand_can_be_used("大火", Player(shield=4))
        assert self.check_hand_can_be_used("大火", Player(shield=3, spark=2))
        assert self.check_hand_can_be_used("大火", Player(qi=1, spark=2))
        assert not self.check_hand_can_be_used("大火", Player(shield=3, spark=1))
        assert not self.check_hand_can_be_used("大火", Player(shield=3, battery=3))
        assert self.check_hand_can_be_used("Shining", Player(shield=6))
        assert self.check_hand_can_be_used("Shining", Player(shield=3, battery=2))
        assert not self.check_hand_can_be_used("Shining", Player(qi=1, spark=2))
        assert not self.check_hand_can_be_used("Shining", Player(shield=3, spark=3))
        assert self.check_hand_can_be_used("Shining", Player(shield=3, battery=3))