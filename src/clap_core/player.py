class Player:
    
    uses_anytime_list = [ "气", "盾" ]

    uses_qi_dict = { "gi":1, "破":2, "冷风":3, "如来":5, "黑洞":8 }

    uses_shield_dict = { "小火":2, "闪电":3, "大火":4, "Shining":6 }

    def __init__(self) -> None:
        self.qi = 0
        self.shield = 0
        self.spark = 0
        self.battery = 0
    
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
