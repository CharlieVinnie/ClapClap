from dataclasses import dataclass, field
from typing import Dict, Tuple, Optional
from .constants import Move, Resource, MOVE_COSTS, ATTACK_POWER, SHIELD_KILLERS, SHI_ZI_FANG_KILLERS, ATTACK_MOVES

@dataclass
class PlayerState:
    resources: Dict[Resource, int] = field(default_factory=lambda: {
        Resource.QI: 0,
        Resource.SHIELD: 0,
        Resource.SPARK: 0,
        Resource.BATTERY: 0,
        Resource.DUCK: 2
    })

    def can_afford(self, move: Move) -> bool:
        if move == Move.DA_HUO:
            # 4 Shield OR 2 Sparks
            if self.resources[Resource.SPARK] >= 2: return True
            if self.resources[Resource.SHIELD] >= 4: return True
            return False
        if move == Move.SHINING:
            # 6 Shield OR 2 Batteries
            if self.resources[Resource.BATTERY] >= 2: return True
            if self.resources[Resource.SHIELD] >= 6: return True
            return False
        
        cost = MOVE_COSTS[move]
        for res, amount in cost.items():
            if self.resources[res] < amount:
                return False
        return True

    def consume(self, move: Move):
        if move == Move.DA_HUO:
            if self.resources[Resource.SPARK] >= 2:
                self.resources[Resource.SPARK] -= 2
            else:
                self.resources[Resource.SHIELD] -= 4
        elif move == Move.SHINING:
            if self.resources[Resource.BATTERY] >= 2:
                self.resources[Resource.BATTERY] -= 2
            else:
                self.resources[Resource.SHIELD] -= 6
        else:
            cost = MOVE_COSTS[move]
            for res, amount in cost.items():
                self.resources[res] -= amount

    def add_resource(self, res: Resource, amount: int = 1):
        self.resources[res] += amount

@dataclass
class ClapClapState:
    p1: PlayerState = field(default_factory=PlayerState)
    p2: PlayerState = field(default_factory=PlayerState)
    round_num: int = 0
    winner: Optional[int] = None # 1, 2, or None

class GameEngine:
    @staticmethod
    def resolve_round(state: ClapClapState, move1: Move, move2: Move) -> ClapClapState:
        # 1. Check validity
        p1_valid = state.p1.can_afford(move1)
        p2_valid = state.p2.can_afford(move2)
        
        if not p1_valid and not p2_valid:
            # Both played illegal moves -> Draw/Mutual Loss
            state.winner = 0
            state.round_num += 1
            return state
        if not p1_valid:
            # P1 played illegal -> P2 wins
            state.winner = 2
            state.round_num += 1
            return state
        if not p2_valid:
            # P2 played illegal -> P1 wins
            state.winner = 1
            state.round_num += 1
            return state
        
        # 2. Consume resources (Both valid now)
        state.p1.consume(move1)
        state.p2.consume(move2)
        
        # 3. Resource Generation (Base)
        # Rule 7: Qi adds 1 qi, Shield adds 1 shield
        if move1 == Move.QI: state.p1.add_resource(Resource.QI)
        if move2 == Move.QI: state.p2.add_resource(Resource.QI)
        if move1 == Move.SHIELD: state.p1.add_resource(Resource.SHIELD)
        if move2 == Move.SHIELD: state.p2.add_resource(Resource.SHIELD)

        # Rule 16/17: Element Gathering
        # Need to determine if Lightning was "eaten" before awarding Battery
        p1_lightning_eaten = False
        p2_lightning_eaten = False
        
        # Check interactions to determine "eaten" status for Lightning
        if move1 == Move.SHAN_DIAN:
            # Rule 17: If eaten by Chi or ShuangChi (implied by "eats Lightning"), no battery.
            if move2 in [Move.CHI, Move.SHUANG_CHI]:
                p1_lightning_eaten = True
        
        if move2 == Move.SHAN_DIAN:
            if move1 in [Move.CHI, Move.SHUANG_CHI]:
                p2_lightning_eaten = True

        # Award Elements
        if move1 == Move.XIAO_HUO: state.p1.add_resource(Resource.SPARK)
        if move2 == Move.XIAO_HUO: state.p2.add_resource(Resource.SPARK)
        
        if move1 == Move.SHAN_DIAN and not p1_lightning_eaten:
            state.p1.add_resource(Resource.BATTERY)
        if move2 == Move.SHAN_DIAN and not p2_lightning_eaten:
            state.p2.add_resource(Resource.BATTERY)

        # 4. Combat Logic
        # Determine if anyone dies
        p1_dead = False
        p2_dead = False

        # Symmetric evaluation
        p1_dead = GameEngine.check_death(move1, move2) # Does P1 die from P2's move?
        p2_dead = GameEngine.check_death(move2, move1) # Does P2 die from P1's move?

        if p1_dead and not p2_dead:
            state.winner = 2
        elif p2_dead and not p1_dead:
            state.winner = 1
        elif p1_dead and p2_dead:
            # Mutual destruction - Draw? Or continue? 
            # Rule 4: Game ends when ONE of the player wins.
            # Usually mutual death is a Draw or both lose. Let's set winner=0 (Draw) or handle as specific logic.
            # I will assume no winner, game ends = Draw.
            state.winner = 0 
        
        state.round_num += 1
        return state

    @staticmethod
    def check_death(defense_move: Move, attack_move: Move) -> bool:
        """Returns True if defense_move is killed by attack_move."""
        
        # If attacker is not attacking, defender is safe (mostly)
        # Exception: Some games have self-destructs, but not here.
        if attack_move not in ATTACK_MOVES and attack_move not in [Move.CHI, Move.SHUANG_CHI]:
             # Chi/ShuangChi are special attacks
             pass
        
        # Handle Attacks vs Attacks
        if defense_move in ATTACK_MOVES and attack_move in ATTACK_MOVES:
            # Rule 11: Stronger wins
            def_p = ATTACK_POWER[defense_move]
            att_p = ATTACK_POWER[attack_move]
            return att_p > def_p
            
        # Handle Defense/Resource vs Attacks
        if attack_move in ATTACK_MOVES:
            # Rule 12: All attacks kill Qi
            if defense_move == Move.QI:
                return True
            
            # Rule 12: Stronger/Equal to Po kills Shield
            if defense_move == Move.SHIELD:
                return attack_move in SHIELD_KILLERS
            
            # Rule 13: Shan ducks all attacks
            if defense_move == Move.SHAN:
                return False
                
            # Rule 12: Stronger/Equal to RuLai kills ShiZiFang
            if defense_move == Move.SHI_ZI_FANG:
                return attack_move in SHI_ZI_FANG_KILLERS
            
            # Chi Interactions
            if defense_move == Move.CHI:
                # Rule 14: Chi kills Po (so Chi survives Po?) -> No, "Chi kills Po" means if Chi attacks Po.
                # Here Chi is defending against Attack.
                # Rule 14: "is killed by all other attack hands" (except Po and Lightning?)
                if attack_move == Move.PO:
                    return False # Chi beats Po (Mutually? Or Chi blocks Po?) 
                    # "Chi kills Po" usually implies Chi wins. If Chi wins, Chi doesn't die.
                if attack_move == Move.SHAN_DIAN:
                    return False # Chi eats Lightning
                return True # Dies to everything else (Gi, XiaoHuo, LengFeng, DaHuo, RuLai, Shining, HeiDong)

            # Shuang Chi Interactions
            if defense_move == Move.SHUANG_CHI:
                # Rule 15: Kills Po, Eats Lightning and Shining.
                if attack_move == Move.PO: return False
                if attack_move == Move.SHAN_DIAN: return False
                if attack_move == Move.SHINING: return False
                # Rule 50: All attacks BESIDES Po, ShanDian, Shining kill ShuangChi
                return True

        # Handle Chi/ShuangChi acting as attackers (against Attacks)
        if attack_move == Move.CHI:
            # Rule 14: Chi kills Po
            if defense_move == Move.PO: return True
            # Chi vs Lightning -> "Eats" (Game continues, implying no death for Lightning either?)
            # Caveat: "Chi eats Lightning with the game continuing". So Lightning does NOT die.
            return False 

        if attack_move == Move.SHUANG_CHI:
            # Rule 15: Kills Po
            if defense_move == Move.PO: return True
            # Eats Lightning/Shining -> Game continues
            return False

        # If attacker is passive (Qi, Shield, etc), defender lives
        return False
