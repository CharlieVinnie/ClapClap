from clap_core.hands import HANDS, kills, Hand

class TestComparingHands:

    def assert_same(self, hand_1: Hand, hand_2: Hand):
        return not kills(hand_1,hand_2) and not kills(hand_1,hand_2)

    def test_comparing_hands(self):

        hand_sequence = [ HANDS["气"], HANDS["gi"], HANDS["破"], HANDS["冷风"], HANDS["如来"], HANDS["黑洞"] ]

        for i in range(len(hand_sequence)):
            for j in range(len(hand_sequence)):
                if i > j :
                    assert kills( hand_sequence[i], hand_sequence[j] )
                else:
                    assert not kills( hand_sequence[i], hand_sequence[j] )
        
        for hand in HANDS.values():
            self.assert_same(hand,hand)

        self.assert_same( HANDS["气"], HANDS["盾"] )
        self.assert_same( HANDS["gi"], HANDS["小火"] )
        self.assert_same( HANDS["闪电"], HANDS["破"] )
        self.assert_same( HANDS["冷风"], HANDS["大火"] )
        self.assert_same( HANDS["如来"], HANDS["Shining"] )