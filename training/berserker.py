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

import numpy as np
from ray.rllib.policy.policy import Policy

class BerserkerPolicy(Policy):
    """
    RLLib Policy wrapper for BerserkerBot.
    """
    def __init__(self, observation_space, action_space, config):
        super().__init__(observation_space, action_space, config)
        self.bot = BerserkerBot()

    def compute_actions(self,
                        obs_batch,
                        state_batches=None,
                        prev_action_batch=None,
                        prev_reward_batch=None,
                        info_batch=None,
                        episodes=None,
                        **kwargs):
        
        actions = []
        for obs in obs_batch:
            # obs might be a Dict or flattened depending on preprocessing.
            # In our case, it should be the Dict from the Env: {'observations': [...], 'action_mask': [...]}
            # But RLLib usually batches these. So `obs_batch` is likely a Dict of arrays if using Dict space?
            # OR, `obs` is a single item if we iterate? No, `obs_batch` is a struct (dict) of data normally.
            # Wait, `compute_actions` receives `obs_batch` which is typically a DataStruct (e.g. Dict of np.arrays).
            # But loop `for obs in obs_batch:` usually implies it's a list or array?
            # Actually, if Obs Space is Dict, `obs_batch` is a dict. Iterating a dict gives keys. That's bad.
            
            # Use specific extraction:
            # If obs_batch is a dict (keys: 'observations', 'action_mask')
            # features = obs_batch['observations']
            pass
        
        # Correct approach for batching:
        # If Dict space, extract the 'observations' component
        # But wait, `obs_batch` passed to `compute_actions` might be a numpy array if Preprocessor flattened it?
        # PPO config usually includes ModelCatalog.
        # Let's assume for now we handle the raw input.
        
        # HACK: For MVP, assume we can access 'observations' key if present.
        
        # Check type
        features = None
        if isinstance(obs_batch, dict) and "observations" in obs_batch:
             features = obs_batch["observations"]
        elif hasattr(obs_batch, "keys") and "observations" in obs_batch.keys():
             features = obs_batch["observations"]
        else:
             # Maybe it IS the feature vector?
             features = obs_batch
             
        # features is (Batch, 2)
        n_batches = len(features)
        
        for i in range(n_batches):
            feat = features[i]
            # feat[0] = Qi, feat[1] = Shield
            state = PlayerState()
            state.resources[Resource.QI] = int(feat[0])
            state.resources[Resource.SHIELD] = int(feat[1])
            # Assuming Spark/Battery are further down if space expanded, but currently only first 2 used by bot?
            # Bot uses can_afford. can_afford checks ALL resources.
            # Observation vector in env.py:
            # [p_self.qi, p_self.shield, p_self.spark, p_self.battery, p_opp...]
            # Indices: 0, 1, 2, 3.
            
            if len(feat) > 2:
                state.resources[Resource.SPARK] = int(feat[2])
                state.resources[Resource.BATTERY] = int(feat[3])
            
            move = self.bot.get_action(state)
            actions.append(list(Move).index(move))
            
        return np.array(actions), [], {}
