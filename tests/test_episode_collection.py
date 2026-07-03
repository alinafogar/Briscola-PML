import unittest

from experiments import collect_observations, play_synthetic_game
from opponents import AGGRESSIVE_THETA, RandomOpponent, ThetaSoftmaxOpponent


class EpisodeCollectionTest(unittest.TestCase):
    def test_synthetic_games_produce_observed_moves(self) -> None:
        result = play_synthetic_game(
            observed_model=ThetaSoftmaxOpponent(AGGRESSIVE_THETA, seed=2),
            observer_model=RandomOpponent(seed=1),
            seed=11,
            observer_player=0,
            observed_player=1,
            theta_name="aggressive",
        )
        observations = collect_observations(
            observed_model=RandomOpponent(seed=3),
            observer_model=RandomOpponent(seed=4),
            num_games=2,
            seed=12,
        )

        self.assertEqual(len(result.trick_history), 20)
        self.assertEqual(sum(result.final_scores), 120)
        self.assertEqual(len(result.observations), 20)
        self.assertTrue(all(move.player == 1 for move in result.observations))
        self.assertTrue(all(move.chosen_card in move.legal_cards for move in result.observations))
        self.assertEqual(len(observations), 40)


if __name__ == "__main__":
    unittest.main()
