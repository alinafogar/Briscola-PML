import unittest

from scripts.run_comparison import summarize_rows


class ComparisonScriptTest(unittest.TestCase):
    def test_summarize_rows_groups_by_feature_set_and_profile(self) -> None:
        rows = [
            {
                "feature_set": "core",
                "profile": "conservative",
                "feature_count": 4,
                "theta_l2_error": 1.0,
                "heldout_loglik_delta": 10.0,
                "heldout_mean_logp_delta": 0.1,
                "calibration_ece": 0.01,
                "importance_ess": 100.0,
                "final_elbo": -20.0,
                "best_elbo": -15.0,
            },
            {
                "feature_set": "core",
                "profile": "conservative",
                "feature_count": 4,
                "theta_l2_error": 3.0,
                "heldout_loglik_delta": 20.0,
                "heldout_mean_logp_delta": 0.2,
                "calibration_ece": 0.03,
                "importance_ess": 200.0,
                "final_elbo": -10.0,
                "best_elbo": -8.0,
            },
        ]

        summary = summarize_rows(rows)

        self.assertEqual(len(summary), 1)
        self.assertEqual(summary[0]["feature_set"], "core")
        self.assertEqual(summary[0]["profile"], "conservative")
        self.assertEqual(summary[0]["runs"], 2)
        self.assertEqual(summary[0]["theta_l2_error_mean"], 2.0)
        self.assertEqual(summary[0]["heldout_loglik_delta_mean"], 15.0)
        self.assertEqual(summary[0]["best_elbo_mean"], -11.5)
        self.assertGreater(summary[0]["theta_l2_error_std"], 0.0)


if __name__ == "__main__":
    unittest.main()
