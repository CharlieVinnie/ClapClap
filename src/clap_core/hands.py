class Hand:
    
    def __init__(self, *, attack_strength: int, defense_strength: int) -> None:
        self.attack_strength = attack_strength
        self.defense_strength = defense_strength

HANDS = {
    "气": Hand(attack_strength=0, defense_strength=0),
    "gi": Hand(attack_strength=1, defense_strength=1),
    "破": Hand(attack_strength=2, defense_strength=2),
    "冷风": Hand(attack_strength=3, defense_strength=3),
    "如来": Hand(attack_strength=4, defense_strength=4),
    "黑洞": Hand(attack_strength=5, defense_strength=5),
    "盾": Hand(attack_strength=0, defense_strength=1),
    "小火": Hand(attack_strength=1, defense_strength=1),
    "闪电": Hand(attack_strength=2, defense_strength=2),
    "大火": Hand(attack_strength=3, defense_strength=3),
    "Shining": Hand(attack_strength=4, defense_strength=4),
}

def kills(hand_1: Hand, hand_2: Hand):
    return hand_1.attack_strength > hand_2.defense_strength