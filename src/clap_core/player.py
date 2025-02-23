class IllegalHandError(Exception):
    pass

class Player:
    
    uses_anytime_list = [ "气", "盾" ]

    uses_qi_dict = { "gi":1, "破":2, "冷风":3, "如来":5, "黑洞":8 }

    uses_shield_dict = { "小火":2, "闪电":3, "大火":4, "Shining":6 }

    def __init__(self, qi:int = 0, shield:int = 0, spark:int = 0, battery:int = 0) -> None:
        self.qi = qi
        self.shield = shield
        self.spark = spark
        self.battery = battery
    
    def __eq__(self, other: object):
        if not isinstance(other, Player):
            raise NotImplementedError
        return (self.qi, self.shield, self.spark, self.battery) == \
               (other.qi, other.shield, other.spark, other.battery)

    def canPlay(self, hand: str):
        if hand == "大火" and self.spark >= 2:
            return True
        if hand == "Shining" and self.battery >= 2:
            return True
        
        if hand in self.uses_anytime_list:
            return True
        
        if hand in self.uses_qi_dict.keys() and self.qi >= self.uses_qi_dict[hand]:
            return True
        if hand in self.uses_shield_dict.keys() and self.shield >= self.uses_shield_dict[hand]:
            return True
        
        return False

    def play(self, hand: str):
        if not self.canPlay(hand):
            raise IllegalHandError(f"Illegal hand: {(self.qi,self.shield,self.spark,self.battery)} tried to play {hand}")

        if hand == "大火" and self.spark >= 2:
            self.spark -= 2
        elif hand == "Shining" and self.battery >= 2:
            self.battery -= 2
        elif hand == "气":
            self.qi += 1
        elif hand == "盾":
            self.shield += 1
        elif hand in self.uses_qi_dict.keys() and self.qi >= self.uses_qi_dict[hand]:
            self.qi -= self.uses_qi_dict[hand]
        elif hand in self.uses_shield_dict.keys() and self.shield >= self.uses_shield_dict[hand]:
            self.shield -= self.uses_shield_dict[hand]
        else:
            raise Exception("Unexpected hand: should not reach here")
        
        if hand == "小火":
            self.spark += 1
        elif hand == "闪电":
            self.battery += 1
