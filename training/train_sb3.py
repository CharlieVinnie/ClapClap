import os
import glob
import random
# Prevent Torch/Numpy-OpenMP deadlock on small machines
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import numpy as np
import gymnasium as gym
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv
from sb3_contrib import MaskablePPO
from clapclap.env import ClapClapEnv
from training.sb3_wrapper import ClapClapSB3Wrapper
from training.berserker import BerserkerBot, StochasticBot
from clapclap.constants import Resource, Move

LOG_DIR = "./sb3_results"
LEAGUE_DIR = os.path.join(LOG_DIR, "league")
os.makedirs(LEAGUE_DIR, exist_ok=True)

class LeagueManager:
    def __init__(self, league_dir):
        self.league_dir = league_dir
        self.snapshots = []
        # Load existing
        self.refresh()
        
    def refresh(self):
        # Glob snapshots
        snaps = glob.glob(os.path.join(self.league_dir, "*.zip"))
        # Sort by iteration number (iter_N.zip)
        # Handle potential non-matching files gracefully
        def get_iter_num(x):
            try:
                # basename -> remove extension -> split by _ -> last part -> int
                return int(os.path.splitext(os.path.basename(x))[0].split('_')[-1])
            except (ValueError, IndexError):
                return -1
                
        self.snapshots = sorted(snaps, key=get_iter_num)
        print(f"League Manager: Found {len(self.snapshots)} opponents (Newest: {os.path.basename(self.snapshots[-1]) if self.snapshots else 'None'}).")
        
    def add_snapshot(self, model, name):
        path = os.path.join(self.league_dir, name)
        model.save(path)
        self.refresh()
        
    def get_opponent(self):
        """
        Returns an opponent Policy or Bot.
        Probabilities:
          - 50%: League Policy (Self-Play)
          - 45%: Stochastic Bots (Heuristic Mix)
          - 5%: BerserkerBot (Baseline)
        """
        r = random.random()
        
        # 5% Berserker
        if r < 0.05:
            return BerserkerBot()
            
        # 10% Stochastic Bot Mix
        if r < 0.15:
            # Create a random bot
            # p (Qi) + q (Shield) <= 1.0
            # Let's generate diverse bots
            # High Aggro: p=0.2, q=0.1 => 70% Attack
            # Turtle: p=0.2, q=0.7 => 10% Attack
            # Balanced: p=0.4, q=0.4 => 20% Attack
            
            # Simple random sampling:
            p = random.uniform(0.1, 0.5)
            q = random.uniform(0.1, 0.5)
            # Ensure p+q <= 1.0 (it usually will be with range 0.5, but clamp)
            if p + q > 0.95: q = 0.95 - p
            
            return StochasticBot(p_qi=p, q_shield=q)
        
        # 85% League (Self-Play)
        # Verify we have snapshots
        if len(self.snapshots) > 0:
            # Bias towards recent models (The Ladder)
            # 80% Chance: Sample from Top 20% (Recent)
            # 20% Chance: Sample from All (Historical/Forgetfulness Check)
            
            n = len(self.snapshots)
            if random.random() < 0.8:
                # Top 20% (at least last 1)
                cutoff = max(1, int(n * 0.2))
                snapshot_path = random.choice(self.snapshots[-cutoff:])
            else:
                # Historical
                snapshot_path = random.choice(self.snapshots)
                
            opponent_model = MaskablePPO.load(snapshot_path, device="cpu")
            return opponent_model.policy
        else:
            # Fallback if no league yet: use Berserker
            return BerserkerBot()

def make_env():
    env = ClapClapEnv(max_cycles=100)
    env = ClapClapSB3Wrapper(env)
    env = Monitor(env, LOG_DIR)
    return env

def sample_game(env, model):
    """
    Play one game and print moves to console.
    """
    obs, _ = env.reset()
    done = False
    print("\n--- SAMPLE GAME START ---")
    round_num = 1
    
    # We need access to the inner wrapper to see opponent moves easily, 
    # OR we just print what happened based on state changes.
    # Simpler: just print the moves as we step. 
    # But step() only takes P0 action. The wrapper handles P1.
    # To start, let's just trace the resource changes or winning.
    # Actually, we can get more info if we just loop.
    
    while not done:
        # P0 Action
        action_masks = obs["action_mask"]
        action, _ = model.predict(obs, action_masks=action_masks, deterministic=True)
        if not isinstance(action, (int, np.integer)): action = action.item()
        
        # Step
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        
        # We can try to infer moves or just print minimal info
        # Accessing the inner env's state is better.
        # wrapper -> Monitor -> ClapClapSB3Wrapper -> ClapClapEnv -> state_manager
        
        inner_env = env.env.env # Monitor.env -> Wrapper.env
        p1 = inner_env.state_manager.p1
        p2 = inner_env.state_manager.p2
        
        # Decode moves
        move_p0 = list(Move)[action]
        move_p1 = list(Move)[info["opponent_move"]]
        
        print(f"R{round_num}: P0[{move_p0.value}] vs P1[{move_p1.value}] || Res: P0(Qi={p1.resources[Resource.QI]}, Sh={p1.resources[Resource.SHIELD]}) P1(Qi={p2.resources[Resource.QI]}, Sh={p2.resources[Resource.SHIELD]})")
        round_num += 1
        
    winner = inner_env.state_manager.winner
    if winner == 1: result = "VICTORY (P0)"
    elif winner == 2: result = "DEFEAT (P1)"
    else: result = "DRAW"
    print(f"--- SAMPLE GAME END: {result} ---\n")

def train():
    print("Creating Environment...")
    # DummyVecEnv wraps the gym env
    vec_env = DummyVecEnv([make_env])
    
    # Initialize League
    league = LeagueManager(LEAGUE_DIR)
    
    print("Initializing Agent...")
    model = MaskablePPO(
        "MultiInputPolicy",
        vec_env,
        verbose=1,
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=64,
        gamma=0.99,
        ent_coef=0.02, # Force exploration (prevent shield spam)
        tensorboard_log=LOG_DIR
    )
    
    iters = 40
    steps_per_iter = 16384 # Shorter iterations for faster feedback
    
    print(f"Starting League Training for {iters} iterations (steps={steps_per_iter})...")
    
    for i in range(iters):
        # 1. Sample Opponent
        opponent = league.get_opponent()
        if isinstance(opponent, BerserkerBot):
            opp_name = "BerserkerBot"
        elif isinstance(opponent, StochasticBot):
            opp_name = f"StochBot(p={opponent.p_qi:.2f},q={opponent.q_shield:.2f})"
        else:
            opp_name = "LeagueAgent"
            
        print(f"--- Iteration {i+1}/{iters} | Opponent: {opp_name} ---")
        
        # 2. Update Env
        # wrapper is inside vec_env -> envs[0] (Monitor) -> env (ClapClapSB3Wrapper)
        vec_env.envs[0].env.set_opponent(opponent)
        
        # 3. Train
        model.learn(total_timesteps=steps_per_iter, reset_num_timesteps=False)
        
        # 4. Save to League
        league.add_snapshot(model, f"iter_{i+1}")
        
        # 5. Sample Game
        sample_game(vec_env.envs[0], model)
        
        # CRITICAL: Reset the VecEnv after "manual play" so it's fresh for PPO
        # PPO requires _last_obs to be valid for the new step.
        obs = vec_env.reset()
        model._last_obs = obs
        
    print("Saving Final Model...")
    model.save(os.path.join(LOG_DIR, "final_model"))
    print("Done.")

if __name__ == "__main__":
    train()
