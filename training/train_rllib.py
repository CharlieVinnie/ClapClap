import ray
from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.env.multi_agent_env import MultiAgentEnv
from clapclap.env import ClapClapEnv
from training.berserker import BerserkerPolicy
import os
import numpy as np

# Custom Wrapper for ParallelPettingZoo -> RLLib MultiAgentEnv
class PettingZooParallelWrapper(MultiAgentEnv):
    def __init__(self, env):
        super().__init__()
        self.env = env
        self.max_cycles = env.max_cycles
        # Copy strict spaces
        self.observation_space = env.observation_spaces
        self.action_space = env.action_spaces
        self._agent_ids = env.possible_agents

    def reset(self, *, seed=None, options=None):
        obs, info = self.env.reset(seed=seed, options=options)
        return obs, info

    def step(self, action_dict):
        obs, rewards, terms, truncs, infos = self.env.step(action_dict)
        
        # RLLib requires "__all__" in terminateds and truncateds
        # ClapClapEnv likely terminates everyone together, so __all__ = any(terms)
        terms["__all__"] = all(terms.values())
        truncs["__all__"] = all(truncs.values())
        
        return obs, rewards, terms, truncs, infos

STORAGE_PATH = os.path.abspath("./ray_results")

def run():
    print("Initializing Ray...")
    ray.init()
    
    print("Registering Env...")
    def env_creator(config):
        return PettingZooParallelWrapper(ClapClapEnv(max_cycles=100))
    
    from ray.tune.registry import register_env
    register_env("clapclap", env_creator)
    
    # Create Dummy
    dummy = env_creator({})
    dummy.reset()
    obs_space = dummy.observation_space["player_0"]
    act_space = dummy.action_space["player_0"]
    
    print("Configuring PPO...")
    config = (
        PPOConfig()
        .environment("clapclap")
        .framework("torch")
        .env_runners(num_env_runners=0)
        .multi_agent(
            policies={
                "main_policy": (None, obs_space, act_space, {}),
                "berserker_policy": (BerserkerPolicy, obs_space, act_space, {}),
            },
            policy_mapping_fn=lambda aid, *args, **kwargs: "main_policy" if aid == "player_0" else "berserker_policy",
            policies_to_train=["main_policy"],
        )
        .training(
            train_batch_size=256,
            gamma=0.99,
            lr=0.0001,
        )
    )
    
    print("Building Algo...")
    algo = config.build()
    
    print("Starting Training Loop...")
    for i in range(5):
        print(f"--- Starting Iteration {i} ---")
        result = algo.train()
        print(f"--- Finished Iteration {i} ---")
        
        mean_reward = result.get('episode_reward_mean', result.get('episode_return_mean', 0.0))
        print(f"Iter {i}: Reward = {mean_reward:.3f}")
        
    ray.shutdown()

if __name__ == "__main__":
    run()
