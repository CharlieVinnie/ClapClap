from clap_core.judge import Judge, GameStatus
from clap_core.hands import HANDS

class TestJudge:

    def test_simplest_game(self):

        judge = Judge()

        judge.play( HANDS["气"], HANDS["气"] )

        assert judge.gameStatus() == GameStatus.ONGOING

        judge.play( HANDS["gi"], HANDS["气"] )

        assert judge.gameStatus() == GameStatus.FIRSTWIN