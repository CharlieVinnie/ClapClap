from clap_core.player import Player

class TestHandsUsing:

    def check_hand_can_be_used(self, hand: str, qi: int = 0, shield: int = 0, spark: int = 0, battery: int = 0):
        player = Player()
        player.qi = qi
        player.shield = shield
        player.spark = spark
        player.battery = battery
        return player.canPlay(hand)

    def test_can_use_hands(self):
        
        assert self.check_hand_can_be_used(hand="气")
        assert self.check_hand_can_be_used(hand="盾")

        assert self.check_hand_can_be_used(hand="气", qi=1, spark=2)

        assert self.check_hand_can_be_used(hand="gi", qi=1)
        assert not self.check_hand_can_be_used(hand="gi", shield=1)

        assert self.check_hand_can_be_used(hand="破", qi=2)
        assert not self.check_hand_can_be_used(hand="破", qi=1, shield=2)

        assert self.check_hand_can_be_used(hand="黑洞", qi=8)
        assert not self.check_hand_can_be_used(hand="黑洞", qi=6, shield=8)

        assert self.check_hand_can_be_used(hand="小火", shield=2)
        assert not self.check_hand_can_be_used(hand="小火", qi=2, shield=1)
        
        assert self.check_hand_can_be_used(hand="大火", shield=4)
        assert self.check_hand_can_be_used(hand="大火", shield=3, spark=2)
        assert self.check_hand_can_be_used(hand="大火", qi=1, spark=2)
        assert not self.check_hand_can_be_used(hand="大火", shield=3, spark=1)
        assert not self.check_hand_can_be_used(hand="大火", shield=3, battery=3)

        assert self.check_hand_can_be_used(hand="Shining", shield=6)
        assert self.check_hand_can_be_used(hand="Shining", shield=3, battery=2)
        assert not self.check_hand_can_be_used(hand="Shining", qi=1, spark=2)
        assert not self.check_hand_can_be_used(hand="Shining", shield=3, spark=3)
        assert self.check_hand_can_be_used(hand="Shining", shield=3, battery=3)