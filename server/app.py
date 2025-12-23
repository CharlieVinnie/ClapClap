from flask import Flask, render_template, jsonify, request
import gymnasium as gym
from sb3_contrib import MaskablePPO
import numpy as np
import os
from clapclap.env import ClapClapEnv
from clapclap.constants import Resource, Move


import uuid
from flask import Flask, render_template, jsonify, request, session

# ... imports ...

app = Flask(__name__)
app.secret_key = os.urandom(24) # Standard secure key generation

# Global Store for Games (InMemory)
# Key: session_id (str), Value: GameSession instance
GAMES = {}

class GameSession:
    # ... (Keep existing logic, but remove global instantiation) ...
    def __init__(self):
        self.env = ClapClapEnv(max_cycles=100)
        self.model = MaskablePPO.load("sb3_results/final_model", device="cpu")
        self.obs = None
        self.done = False
        self.history = []
        self.reset() # Auto-reset on init

    def reset(self):
        self.obs, _ = self.env.reset()
        self.done = False
        self.history = []
        return self.get_state()
        
    def step(self, human_move_name):
        # ... (Keep existing logic) ...
        if self.done: return self.get_state()
        
        # 1. Human Action (Player 1)
        try:
            human_move = Move[human_move_name.upper()]
        except KeyError:
            return {"error": "Invalid Move"}
            
        human_action_idx = list(Move).index(human_move)
        
        # 2. Agent Action (Player 0)
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
        p0_res = self.env.state_manager.p1.resources.copy()
        p1_res = self.env.state_manager.p2.resources.copy()
        
        round_res = {
            "round": self.env.state_manager.round_num,
            "agent_move": agent_move.value, 
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
        # ... (Same as before) ...
        # Ensure we handle init case where obs might be None if reset wasn't called (but we call it in init now)
        if self.obs is None: self.reset()

        p0 = self.env.state_manager.p1
        p1 = self.env.state_manager.p2 
        
        p1_mask = self.obs["player_1"]["action_mask"]
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

def get_session():
    if 'uid' not in session:
        session['uid'] = str(uuid.uuid4())
    
    uid = session['uid']
    if uid not in GAMES:
        GAMES[uid] = GameSession()
    return GAMES[uid]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/reset', methods=['POST'])
def reset():
    game = get_session()
    return jsonify(game.reset())

@app.route('/step', methods=['POST'])
def step():
    data = request.json
    move = data.get('move')
    game = get_session()
    return jsonify(game.step(move))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
