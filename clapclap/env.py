import functools
import gymnasium
from gymnasium import spaces
from pettingzoo import ParallelEnv
import numpy as np
from .game import GameEngine, ClapClapState, PlayerState
from .constants import Move, Resource, ATTACK_POWER

class ClapClapEnv(ParallelEnv):
    metadata = {"render_modes": ["human"], "name": "clapclap_v0"}

    def __init__(self, render_mode=None):
        self.possible_agents = ["player_0", "player_1"]
        self.render_mode = render_mode
        self.state_manager = ClapClapState()
        
        # Observation: [Qi, Shield, Spark, Battery, Duck] x 2 players
        # + Round Num?
        self.observation_spaces = {
            agent: spaces.Box(low=0, high=100, shape=(10,), dtype=np.int32)
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
        return self._get_obs(), {}

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
        rewards = {agent: 0 for agent in self.agents}
        
        if self.state_manager.winner is not None:
            # Game Over
            terminations = {agent: True for agent in self.agents}
            if self.state_manager.winner == 1:
                rewards["player_0"] = 1
                rewards["player_1"] = -1
            elif self.state_manager.winner == 2:
                rewards["player_0"] = -1
                rewards["player_1"] = 1
            else:
                # Draw (winner=0)
                rewards["player_0"] = 0
                rewards["player_1"] = 0
                
        # Optional: Truncate if too many rounds to prevent infinite loops?
        if self.state_manager.round_num > 100:
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
        
        # Relative obs? Or Absolute?
        # Player 0 sees P1 then P2
        # Player 1 sees P2 then P1 (usually symmetric view preferred)
        
        obs_0 = np.array(p1_vec + p2_vec, dtype=np.int32)
        obs_1 = np.array(p2_vec + p1_vec, dtype=np.int32)
        
        return {"player_0": obs_0, "player_1": obs_1}

    def action_mask(self):
        # Return dict of valid action masks
        masks = {}
        for i, agent in enumerate(self.agents):
            p_state = self.state_manager.p1 if i == 0 else self.state_manager.p2
            mask = [p_state.can_afford(m) for m in self.move_list]
            masks[agent] = mask
        return masks
