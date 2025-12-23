from flask import Flask, render_template, jsonify, request
import gymnasium as gym
from sb3_contrib import MaskablePPO
import numpy as np
import os
from clapclap.env import ClapClapEnv
from clapclap.constants import Resource, Move
from training.sb3_wrapper import ClapClapSB3Wrapper # For observation alignment if needed, but we use raw env

app = Flask(__name__)

# Global State
class GameSession:
    def __init__(self):
        self.env = ClapClapEnv(max_cycles=100)
        # We need the Wrapper just to get the Observation Space correctly aligned if we used it for training?
        # The Wrapper adds 'action_mask'Key to the Dict entry.
        # But ClapClapEnv native now provides that too (we added it).
        # Let's check env.py... Yes, we modified ClapClapEnv to return Dict with action_mask.
        # So raw env is fine.
        
        self.model = MaskablePPO.load("sb3_results/final_model", device="cpu")
        self.obs = None
        self.done = False
        self.history = []
        
    def reset(self):
        self.obs, _ = self.env.reset()
        self.done = False
        self.history = []
        return self.get_state()
        
    def step(self, human_move_name):
        if self.done: return self.get_state()
        
        # 1. Human Action (Player 1)
        # Map string to Enum index
        try:
            # Match by value (character) or name?
            # User will likely send "Qi" or "Shield" (names)
            human_move = Move[human_move_name.upper()]
        except KeyError:
            # Maybe they sent the character value?
            # Let's assume Name for now.
            return {"error": "Invalid Move"}
            
        human_action_idx = list(Move).index(human_move)
        
        # 2. Agent Action (Player 0)
        # Agent sees player_0 obs
        agent_obs = self.obs["player_0"]
        agent_mask = agent_obs["action_mask"]
        
        agent_action_idx, _ = self.model.predict(agent_obs, action_masks=agent_mask, deterministic=False)
        if not isinstance(agent_action_idx, (int, np.integer)):
             agent_action_idx = agent_action_idx.item()
             
        agent_move = list(Move)[agent_action_idx]
        
        # 3. Step
        actions = {
            "player_0": agent_action_idx,
            "player_1": human_action_idx
        }
        
        self.obs, rewards, terms, truncs, infos = self.env.step(actions)
        
        # History
        # Record what happened
        # We need resources BEFORE the step? Or after?
        # Let's show Resulting state.
        
        p0_res = self.env.state_manager.p1.resources.copy()
        p1_res = self.env.state_manager.p2.resources.copy()
        
        round_res = {
            "round": self.env.state_manager.round_num,
            "agent_move": agent_move.value, # Character
            "human_move": human_move.value,
            "agent_qi": p0_res[Resource.QI],
            "agent_shield": p0_res[Resource.SHIELD],
            "human_qi": p1_res[Resource.QI],
            "human_shield": p1_res[Resource.SHIELD],
            "winner": self.env.state_manager.winner
        }
        self.history.append(round_res)
        
        self.done = terms["player_0"] or truncs["player_0"]
        return self.get_state()

    def get_state(self):
        # Return current resources for UI
        p0 = self.env.state_manager.p1
        p1 = self.env.state_manager.p2 # Human
        
        # Check available moves for Human (Action Mask)
        # P1 mask
        p1_mask = self.obs["player_1"]["action_mask"]
        # Convert mask to list of available Move Names
        moves = list(Move)
        available_moves = [m.name for i, m in enumerate(moves) if p1_mask[i] == 1]
        
        return {
            "done": self.done,
            "history": self.history,
            "human": {
                "qi": p1.resources[Resource.QI],
                "shield": p1.resources[Resource.SHIELD],
                "spark": p1.resources[Resource.SPARK],
                "duck": p1.resources[Resource.DUCK],
                "battery": p1.resources[Resource.BATTERY]
            },
            "agent": {
                "qi": p0.resources[Resource.QI],
                "shield": p0.resources[Resource.SHIELD],
                "spark": p0.resources[Resource.SPARK],
                "duck": p0.resources[Resource.DUCK],
                "battery": p0.resources[Resource.BATTERY]
            },
            "available_moves": available_moves
        }

SESSION = GameSession()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/reset', methods=['POST'])
def reset():
    return jsonify(SESSION.reset())

@app.route('/step', methods=['POST'])
def step():
    data = request.json
    move = data.get('move')
    return jsonify(SESSION.step(move))

if __name__ == '__main__':
    SESSION.reset()
    app.run(host='0.0.0.0', port=5000)
