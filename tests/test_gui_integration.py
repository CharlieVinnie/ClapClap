import pytest
from server.app import GameSession
from clapclap.constants import Move

class TestGUIIntegration:
    def test_session_step_crash(self):
        """
        Regression Test: Ensure GameSession.step() does not crash accessing round number.
        """
        session = GameSession() # Loads model from file
        initial_state = session.reset()
        assert initial_state["done"] == False
        
        # Step
        # User plays "Qi"
        res = session.step("QI")
        
        # Check History structure
        history = res["history"]
        assert len(history) == 1
        last_entry = history[0]
        
        # This was the crashing line:
        assert "round" in last_entry
        assert isinstance(last_entry["round"], int)
        assert last_entry["round"] == 1
        
        # Check other fields
        assert "human_move" in last_entry
        assert last_entry["human_move"] == Move.QI.value
