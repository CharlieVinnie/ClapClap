class Hand:
    
    def __init__(self, name: str, attack_strength: int, defense_strength: int) -> None:
        self.name = name
        self.attack_strength = attack_strength
        self.defense_strength = defense_strength

__HAND_LIST = [
    Hand(name="气", attack_strength=0, defense_strength=0),
    Hand(name="gi", attack_strength=1, defense_strength=1),
    Hand(name="破", attack_strength=2, defense_strength=2),
    Hand(name="冷风", attack_strength=3, defense_strength=3),
    Hand(name="如来", attack_strength=4, defense_strength=4),
    Hand(name="黑洞", attack_strength=5, defense_strength=5),
    Hand(name="盾", attack_strength=0, defense_strength=1),
    Hand(name="小火", attack_strength=1, defense_strength=1),
    Hand(name="闪电", attack_strength=2, defense_strength=2),
    Hand(name="大火", attack_strength=3, defense_strength=3),
    Hand(name="Shining", attack_strength=4, defense_strength=4),
]

HANDS = { hand.name:hand for hand in __HAND_LIST }

def kills(hand_1: str, hand_2: str):
    return HANDS[hand_1].attack_strength > HANDS[hand_2].defense_strength