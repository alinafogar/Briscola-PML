import unittest

from game import BriscolaGame, Card, PlayedCard, Rank, Suit, trick_winner


class BriscolaEngineTest(unittest.TestCase):
    def test_trick_rules_cover_suit_and_trump_cases(self) -> None:
        self.assertEqual(
            trick_winner(
                PlayedCard(0, Card(Rank.THREE, Suit.CUPS)),
                PlayedCard(1, Card(Rank.ACE, Suit.CUPS)),
                Suit.COINS,
            ),
            1,
        )
        self.assertEqual(
            trick_winner(
                PlayedCard(0, Card(Rank.ACE, Suit.CUPS)),
                PlayedCard(1, Card(Rank.TWO, Suit.COINS)),
                Suit.COINS,
            ),
            1,
        )
        self.assertEqual(
            trick_winner(
                PlayedCard(0, Card(Rank.TWO, Suit.CUPS)),
                PlayedCard(1, Card(Rank.ACE, Suit.SWORDS)),
                Suit.COINS,
            ),
            0,
        )

    def test_full_game_finishes_with_expected_score_total(self) -> None:
        game = BriscolaGame.new(seed=7, first_player=0)

        while not game.finished:
            player = game.public_state().current_player
            assert player is not None
            game.play_card(player, game.legal_moves()[0])

        self.assertEqual(len(game.trick_history), 20)
        self.assertEqual(sum(game.scores), 120)
        self.assertTrue(game.public_state().finished)


if __name__ == "__main__":
    unittest.main()
