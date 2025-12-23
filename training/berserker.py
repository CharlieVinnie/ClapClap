from clapclap.constants import Move, Resource, ATTACK_MOVES
from clapclap.game import PlayerState

class BerserkerBot:
    """
    A simple scripted bot that always charges Qi until it can attack.
    Prefers strongest available attack.
    """
    def get_action(self, state: PlayerState) -> Move:
        # Check what attacks we can afford
        affordable_moves = [m for m in Move if state.can_afford(m)]
        affordable_attacks = [m for m in affordable_moves if m in ATTACK_MOVES]
        
        if affordable_attacks:
            # Pick strongest attack
            # Sort by power (descending)
            from clapclap.constants import ATTACK_POWER
            best_attack = max(affordable_attacks, key=lambda m: ATTACK_POWER[m])
            return best_attack
        
        # If we can't attack, just charge Qi
        return Move.QI

import random
class StochasticBot:
    """
    Plays Qi with p, Shield with q, else Max Attack.
    """
    def __init__(self, p_qi: float, q_shield: float):
        self.p_qi = p_qi
        self.q_shield = q_shield
        
    def get_action(self, state: PlayerState) -> Move:
        r = random.random()
        
        # 1. Try Qi (if affordable, which it always is)
        if r < self.p_qi:
            return Move.QI
            
        # 2. Try Shield (if affordable)
        if r < self.p_qi + self.q_shield:
            if state.can_afford(Move.SHIELD):
                return Move.SHIELD
            # If cant afford, fall through or default?
            # "Plays Shield with q prob" implies intent. If fail, usually default to Qi.
            return Move.QI
            
        # 3. Max Attack
        # "Plays max possible attack with 1-p-q"
        affordable_moves = [m for m in Move if state.can_afford(m)]
        affordable_attacks = [m for m in affordable_moves if m in ATTACK_MOVES]
        
        if affordable_attacks:
            from clapclap.constants import ATTACK_POWER
            # Sort by power descending
            best_attack = max(affordable_attacks, key=lambda m: ATTACK_POWER[m])
            return best_attack
            
        # If no attack possible, default to Qi
        return Move.QI


