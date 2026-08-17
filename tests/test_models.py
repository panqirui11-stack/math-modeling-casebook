import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from modeling_casebook.facility_location import solve_p_median
from modeling_casebook.forecasting import linear_trend_forecast
from modeling_casebook.topsis import topsis


class ModelingTests(unittest.TestCase):
    def test_topsis_prefers_dominant_option(self):
        result = topsis(
            [[9, 9, 2], [7, 6, 5], [5, 7, 8]],
            [0.4, 0.3, 0.3],
            ["benefit", "benefit", "cost"],
        )
        self.assertEqual(result.ranking[0], 0)
        self.assertGreater(result.closeness[0], result.closeness[1])

    def test_p_median_selects_two_endpoints(self):
        result = solve_p_median(
            demand_points=[(0, 0), (10, 0)],
            demand_weights=[1, 1],
            candidate_points=[(0, 0), (5, 0), (10, 0)],
            p=2,
        )
        self.assertEqual(result.selected_indices, (0, 2))
        self.assertEqual(result.objective, 0.0)

    def test_linear_trend_forecast_exact_line(self):
        result = linear_trend_forecast([2, 5, 8, 11], horizon=2)
        self.assertEqual(result.slope, 3.0)
        self.assertEqual(result.forecast, (14.0, 17.0))
        self.assertEqual(result.r_squared, 1.0)


if __name__ == "__main__":
    unittest.main()
