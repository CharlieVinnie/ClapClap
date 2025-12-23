import gymnasium as gym
from gymnasium import spaces
import numpy as np
from clapclap.constants import Move, Resource
from clapclap.game import PlayerState
from training.berserker import BerserkerBot

class ClapClapSB3Wrapper(gym.Env):
    """
    A Single-Agent Wrapper for ClapClap.
    The agent plays as 'player_0', and the opponent ('player_1') is controlled by a Bot.
    """
    metadata = {"render_modes": ["human"]}

    def __init__(self, env):
        super().__init__()
        self.env = env
        self.bot = BerserkerBot()
        
        # Fixed Agents
        self.agent_id = "player_0"
        self.opponent_id = "player_1"
        
        # Spaces
        # PettingZoo ParallelEnv uses methods for spaces
        self.observation_space = self.env.observation_space(self.agent_id)
        self.action_space = self.env.action_space(self.agent_id)
        
        self.opponent_policy = None

    def set_opponent(self, policy):
        """
        Set the opponent policy.
        :param policy: Either a BerserkerBot instance or a stable_baselines3 Policy object.
        """
        if hasattr(policy, "get_action"):
            self.bot = policy
            self.opponent_policy = None
        else:
            self.bot = None
            self.opponent_policy = policy

    def reset(self, seed=None, options=None):
        obs_dict, infos = self.env.reset(seed=seed, options=options)
        self._last_obs = obs_dict
        return obs_dict[self.agent_id], infos[self.agent_id]

    def step(self, action):
        # 1. Get Opponent Move
        # If we have a learned policy
        if self.opponent_policy is not None:
            # Prepare observation for opponent (player_1)
            opp_obs = self._last_obs[self.opponent_id]
            # Predict
            # MaskablePPO policy.predict takes (obs, state, episode_start, action_masks)
            # We strictly need to pass action_masks if we want valid moves.
            action_masks = opp_obs["action_mask"].astype(bool)
            
            # Note: predict() returns (action, state)
            opp_move_idx, _ = self.opponent_policy.predict(
                opp_obs, 
                action_masks=action_masks,
                deterministic=False # Stochastic for diversity
            )
            # opp_move_idx is usually a 0-d array or int
            if not isinstance(opp_move_idx, (int, np.integer)):
                opp_move_idx = opp_move_idx.item()
                
        else:
            # Fallback to BerserkerBot
            # Reconstruct Opponent State from their observation vector
            opp_obs_vec = self._last_obs[self.opponent_id]["observations"]
            
            # Vector Map (from env.py):
            # 0: Qi, 1: Shield, 2: Spark, 3: Battery
            bot_state = PlayerState()
            bot_state.resources[Resource.QI] = int(opp_obs_vec[0])
            bot_state.resources[Resource.SHIELD] = int(opp_obs_vec[1])
            try:
                bot_state.resources[Resource.SPARK] = int(opp_obs_vec[2])
                bot_state.resources[Resource.BATTERY] = int(opp_obs_vec[3])
                bot_state.resources[Resource.DUCK] = int(opp_obs_vec[4])
            except IndexError:
                pass
            
            opp_move_enum = self.bot.get_action(bot_state)
            opp_move_idx = list(Move).index(opp_move_enum)
        
        # 2. Step Environment
        actions = {
            self.agent_id: action,
            self.opponent_id: opp_move_idx
        }
        
        obs_dict, rewards, terms, truncs, infos = self.env.step(actions)
        self._last_obs = obs_dict
        
        # Add opponent move to info for visualization
        infos[self.agent_id]["opponent_move"] = opp_move_idx
        
        # 3. Return results for Player 0
        return (
            obs_dict[self.agent_id],
            rewards[self.agent_id],
            terms[self.agent_id],
            truncs[self.agent_id],
            infos[self.agent_id]
        )

    def action_masks(self):
        """
        Required for MaskablePPO.
        Returns boolean mask for the current state (player_0).
        """
        if self._last_obs is None:
            return np.ones(self.action_space.n, dtype=bool)
        
        # Env returns float mask [0.0, 1.0], convert to bool
        return self._last_obs[self.agent_id]["action_mask"].astype(bool)
