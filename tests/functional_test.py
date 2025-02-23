from clap_core.judge import Judge, GameStatus

class TestJudge:

    def test_simplest_game(self):

        judge = Judge()

        judge.play( "气", "气" )

        assert judge.gameStatus() == GameStatus.ONGOING

        judge.play( "gi", "气" )

        assert judge.gameStatus() == GameStatus.FIRSTWIN