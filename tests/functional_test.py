from clap_core.judge import Judge, GameStatus
from clap_core.hands import HANDS

class TestJudge:

    def test_simplest_game(self):

        judge = Judge()

        judge.play( "气", "气" )

        assert judge.gameStatus() == GameStatus.ONGOING

        judge.play( "gi", "气" )

        assert judge.gameStatus() == GameStatus.FIRSTWIN