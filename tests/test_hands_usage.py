from clap_core.player import Player, IllegalHandError
import pytest

class TestHandsUsing:

    def check_hand_can_be_used(self, hand: str, player_pre: Player, player_post: Player):
        assert player_pre.canPlay(hand)
        player_pre.play(hand)
        assert player_pre == player_post

    def check_hand_cannot_be_used(self, hand: str, player: Player):
        assert not player.canPlay(hand)
        with pytest.raises(IllegalHandError, match=f"Illegal hand:"):
            player.play(hand)

    def test_can_use_hands(self):
        
        self.check_hand_can_be_used("气", Player(qi=0, shield=2), Player(qi=1, shield=2))
        self.check_hand_can_be_used("盾", Player(qi=1, shield=2), Player(qi=1, shield=3))

        self.check_hand_can_be_used("气", Player(qi=1, spark=2), Player(qi=2, spark=2))

        self.check_hand_can_be_used("gi", Player(qi=1), Player())
        self.check_hand_cannot_be_used("gi", Player(shield=1))

        self.check_hand_can_be_used("破", Player(qi=2), Player())
        self.check_hand_cannot_be_used("破", Player(qi=1, shield=2))

        self.check_hand_can_be_used("黑洞", Player(qi=8), Player(qi=0))
        self.check_hand_cannot_be_used("黑洞", Player(qi=7, shield=8))

        self.check_hand_can_be_used("小火", Player(shield=2), Player())
        self.check_hand_cannot_be_used("小火", Player(qi=2, shield=1))

        self.check_hand_can_be_used("大火", Player(shield=4), Player())
        self.check_hand_can_be_used("大火", Player(shield=3, spark=2), Player(shield=3))
        self.check_hand_can_be_used("大火", Player(shield=5, spark=3), Player(shield=5, spark=1))
        self.check_hand_can_be_used("大火", Player(qi=1, spark=2), Player(qi=1))
        self.check_hand_cannot_be_used("大火", Player(shield=3, spark=1))
        self.check_hand_cannot_be_used("大火", Player(shield=3, battery=3))
        
        self.check_hand_can_be_used("Shining", Player(shield=6), Player())
        self.check_hand_can_be_used("Shining", Player(shield=3, battery=2), Player(shield=3))
        self.check_hand_cannot_be_used("Shining", Player(qi=1, spark=2))
        self.check_hand_cannot_be_used("Shining", Player(shield=3, spark=3))
        self.check_hand_can_be_used("Shining", Player(shield=3, battery=3), Player(shield=3, battery=1))