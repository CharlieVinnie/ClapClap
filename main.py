import random
from clapclap.game import GameEngine, ClapClapState
from clapclap.constants import Move, Resource, ATTACK_POWER

def play_game():
    state = ClapClapState()
    print("Starting ClapClap Game!")
    
    while state.winner is None:
        print(f"\n--- Round {state.round_num + 1} ---")
        print(f"P1: {state.p1.resources}")
        print(f"P2: {state.p2.resources}")
        
        # Simple random bot logic
        # Filter moves they can afford
        p1_moves = [m for m in Move if state.p1.can_afford(m)]
        p2_moves = [m for m in Move if state.p2.can_afford(m)]
        
        # Prefer attacks if possible to make it interesting
        p1_attacks = [m for m in p1_moves if m in ATTACK_POWER]
        p2_attacks = [m for m in p2_moves if m in ATTACK_POWER]
        
        m1 = random.choice(p1_attacks if p1_attacks and random.random() > 0.3 else p1_moves)
        m2 = random.choice(p2_attacks if p2_attacks and random.random() > 0.3 else p2_moves)
        
        print(f"P1 plays: {m1.value}")
        print(f"P2 plays: {m2.value}")
        
        state = GameEngine.resolve_round(state, m1, m2)
        
    print(f"\nGame Over! Winner: {state.winner}")
    if state.winner == 0:
        print("Draw!")

if __name__ == "__main__":
    play_game()
