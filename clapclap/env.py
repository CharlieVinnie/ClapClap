import functools
import gymnasium
from gymnasium import spaces
from pettingzoo import ParallelEnv
import numpy as np
from .game import GameEngine, ClapClapState, PlayerState
from .constants import Move, Resource, ATTACK_POWER

class ClapClapEnv(ParallelEnv):
    metadata = {"render_modes": ["human"], "name": "clapclap_v0"}

    def __init__(self, render_mode=None, max_cycles=100):
        self.possible_agents = ["player_0", "player_1"]
        self.render_mode = render_mode
        self.state_manager = ClapClapState()
        self.max_cycles = max_cycles
        
        # Observation: Dict with 'observations' and 'action_mask'
        self.observation_spaces = {
            agent: spaces.Dict({
                "observations": spaces.Box(low=-100, high=100, shape=(10,), dtype=np.float32),
                "action_mask": spaces.Box(0, 1, shape=(len(Move),), dtype=np.float32)
            })
            for agent in self.possible_agents
        }
        
        # Actions: All Moves
        self.action_spaces = {
            agent: spaces.Discrete(len(Move))
            for agent in self.possible_agents
        }
        
        self.move_list = list(Move)

    def reset(self, seed=None, options=None):
        self.agents = self.possible_agents[:]
        self.state_manager = ClapClapState()
        infos = {agent: {} for agent in self.agents}
        return self._get_obs(), infos

    def step(self, actions):
        # Extract moves
        move_0 = self.move_list[actions["player_0"]]
        move_1 = self.move_list[actions["player_1"]]
        
        # Resolve round
        self.state_manager = GameEngine.resolve_round(
            self.state_manager, move_0, move_1
        )
        
        observations = self._get_obs()
        infos = {agent: {} for agent in self.agents}
        
        # Check termination
        terminations = {agent: False for agent in self.agents}
        truncations = {agent: False for agent in self.agents}
        rewards = {agent: 0.0 for agent in self.agents}
        
        # Reward Shaping: Economic Advantage
        # Reward += 0.01 * (My_Qi - Opponent_Qi)
        # Reward += 0.05 * (My_Duck - Opponent_Duck)
        
        # P0 Rewards
        p1 = self.state_manager.p1
        p2 = self.state_manager.p2
        
        rewards["player_0"] += 0.001 * (p1.resources[Resource.QI] - p2.resources[Resource.QI])
        rewards["player_0"] += 0.005 * (p1.resources[Resource.DUCK] - p2.resources[Resource.DUCK])
        
        # P1 Rewards (Symmetric)
        rewards["player_1"] += 0.001 * (p2.resources[Resource.QI] - p1.resources[Resource.QI])
        rewards["player_1"] += 0.005 * (p2.resources[Resource.DUCK] - p1.resources[Resource.DUCK])
        
        # Step Penalty (Encourage Speed / Aggression)
        rewards["player_0"] -= 0.001
        rewards["player_1"] -= 0.001
                
        if self.state_manager.winner is not None:
            # Game Over
            terminations = {agent: True for agent in self.agents}
            if self.state_manager.winner == 1:
                rewards["player_0"] += 1.0
                rewards["player_1"] -= 1.0
                infos["player_0"]["is_success"] = True
                infos["player_1"]["is_success"] = False
            elif self.state_manager.winner == 2:
                rewards["player_0"] -= 1.0
                rewards["player_1"] += 1.0
                infos["player_0"]["is_success"] = False
                infos["player_1"]["is_success"] = True
            else:
                pass # Draw
                
        # Truncate if too many rounds
        if self.state_manager.round_num >= self.max_cycles:
             truncations = {agent: True for agent in self.agents}

        return observations, rewards, terminations, truncations, infos

    def _get_obs(self):
        # Encode state
        def encode_player(p: PlayerState):
            return [
                p.resources[Resource.QI],
                p.resources[Resource.SHIELD],
                p.resources[Resource.SPARK],
                p.resources[Resource.BATTERY],
                p.resources[Resource.DUCK]
            ]
            
        p1_vec = encode_player(self.state_manager.p1)
        p2_vec = encode_player(self.state_manager.p2)
        
        obs_0 = np.array(p1_vec + p2_vec, dtype=np.float32)
        obs_1 = np.array(p2_vec + p1_vec, dtype=np.float32)
        
        # Get masks
        masks = self.action_mask()
        
        return {
            "player_0": {
                "observations": obs_0,
                "action_mask": np.array(masks["player_0"], dtype=np.float32)
            },
            "player_1": {
                "observations": obs_1,
                "action_mask": np.array(masks["player_1"], dtype=np.float32)
            }
        }

    def action_mask(self):
        # Return dict of valid action masks
        masks = {}
        for i, agent in enumerate(self.agents):
            p_curr = self.state_manager.p1 if i == 0 else self.state_manager.p2
            p_opp = self.state_manager.p2 if i == 0 else self.state_manager.p1
            
            mask = [p_curr.can_afford(m) for m in self.move_list]
            
            # Removed Heuristic: Let the agent learn strategy. Only mask illegal moves.
            
            masks[agent] = mask
        return masks
