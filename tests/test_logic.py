import unittest
from clapclap.game import GameEngine, ClapClapState, PlayerState
from clapclap.constants import Move, Resource

class TestClapClapLogic(unittest.TestCase):
    def setUp(self):
        self.state = ClapClapState()

    def test_basic_resources(self):
        # Round 1: Qi vs Qi
        self.state = GameEngine.resolve_round(self.state, Move.QI, Move.QI)
        self.assertEqual(self.state.p1.resources[Resource.QI], 1)
        self.assertEqual(self.state.p2.resources[Resource.QI], 1)
        
        # Round 2: P1 Shield, P2 Qi
        self.state = GameEngine.resolve_round(self.state, Move.SHIELD, Move.QI)
        self.assertEqual(self.state.p1.resources[Resource.SHIELD], 1)
        self.assertEqual(self.state.p2.resources[Resource.QI], 2)

    def test_combat_basic(self):
        # Give resources
        self.state.p1.resources[Resource.QI] = 10
        self.state.p2.resources[Resource.QI] = 10
        
        # Gi (1 Qi) vs Qi
        # Gi > Qi (Attack kills Qi)
        state = GameEngine.resolve_round(self.state, Move.GI, Move.QI)
        self.assertEqual(state.winner, 1)

    def test_shield_interactions(self):
        self.state.p1.resources[Resource.SHIELD] = 10
        self.state.p2.resources[Resource.QI] = 10
        
        # Shield vs Gi (Shield blocks Gi)
        # Gi is 40 power. Po is 60. Gi cannot kill Shield.
        self.state.winner = None
        state = GameEngine.resolve_round(self.state, Move.SHIELD, Move.GI)
        self.assertIsNone(state.winner)
        
        # Shield vs Po (Po kills Shield)
        state = GameEngine.resolve_round(self.state, Move.SHIELD, Move.PO)
        self.assertEqual(state.winner, 2)

    def test_leng_feng_vs_shield(self):
        # Rule 44: Leng Feng kills Shield
        self.state.p1.resources[Resource.SHIELD] = 10
        self.state.p2.resources[Resource.QI] = 10
        state = GameEngine.resolve_round(self.state, Move.SHIELD, Move.LENG_FENG)
        self.assertEqual(state.winner, 2)

    def test_chi_interactions(self):
        self.state.p1.resources[Resource.QI] = 10
        self.state.p2.resources[Resource.QI] = 10
        
        # Chi vs Po => Chi wins (Chi kills Po)
        state = GameEngine.resolve_round(self.state, Move.CHI, Move.PO)
        self.assertEqual(state.winner, 1)
        
        # Chi vs Lightning => Chi "eats" Lightning
        # Game continues (Draw/No Death)
        self.state.winner = None
        state = GameEngine.resolve_round(self.state, Move.CHI, Move.SHAN_DIAN)
        self.assertIsNone(state.winner)
        
        # Chi vs Gi => Chi dies
        state = GameEngine.resolve_round(self.state, Move.CHI, Move.GI)
        self.assertEqual(state.winner, 2)

    def test_lightning_element(self):
        self.state.p1.resources[Resource.SHIELD] = 10
        self.state.p2.resources[Resource.SHIELD] = 10
        
        # Lightning vs Shield (Lightning >= Po, so Lightning kills Shield?)
        # Lightning power = 60. Po = 60.
        # Yes, Lightning kills Shield.
        
        # Let's test Lightning vs Lightning (Clash)
        # Should get batteries
        state = GameEngine.resolve_round(self.state, Move.SHAN_DIAN, Move.SHAN_DIAN)
        self.assertEqual(state.p1.resources[Resource.BATTERY], 1)
        self.assertEqual(state.p2.resources[Resource.BATTERY], 1)
        self.assertIsNone(state.winner)

    def test_lightning_eaten_no_battery(self):
        self.state.p1.resources[Resource.SHIELD] = 10
        self.state.p2.resources[Resource.QI] = 10
        
        # Lightning vs Chi
        # P1 plays Lightning, P2 plays Chi.
        # P2 eats Lightning -> No death. P1 gets NO battery.
        state = GameEngine.resolve_round(self.state, Move.SHAN_DIAN, Move.CHI)
        self.assertEqual(state.p1.resources[Resource.BATTERY], 0)
        self.assertIsNone(state.winner)

    def test_shuang_chi(self):
        self.state.p1.resources[Resource.QI] = 10
        self.state.p2.resources[Resource.SHIELD] = 10
        
        # Shuang Chi vs Shining
        # Eats Shining -> No death.
        state = GameEngine.resolve_round(self.state, Move.SHUANG_CHI, Move.SHINING)
        self.assertIsNone(state.winner)

if __name__ == '__main__':
    unittest.main()
