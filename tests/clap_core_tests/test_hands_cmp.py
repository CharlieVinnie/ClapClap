from clap_core.hands import HANDS, kills

class TestComparingHands:

    def assert_same(self, hand_1: str, hand_2: str):
        return not kills(hand_1,hand_2) and not kills(hand_1,hand_2)

    def test_comparing_hands(self):

        hand_sequence = [ "气", "gi", "破", "冷风", "如来", "黑洞" ]

        for i in range(len(hand_sequence)):
            for j in range(len(hand_sequence)):
                if i > j :
                    assert kills( hand_sequence[i], hand_sequence[j] )
                else:
                    assert not kills( hand_sequence[i], hand_sequence[j] )
        
        for hand in HANDS.keys():
            self.assert_same(hand,hand)

        self.assert_same( "气", "盾" )
        self.assert_same( "gi", "小火" )
        self.assert_same( "闪电", "破" )
        self.assert_same( "冷风", "大火" )
        self.assert_same( "如来", "Shining" )