"""Unittest harness for Unit 03 three-point differentiation workflow."""

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lib.differentiation_tools import DifferentiationTools
from unit03.differentiation.config import FREEFALL_GRAVITY_TOL
from unit03.differentiation.workflow import generate_all_outputs


class TestDifferentiationThreePoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool = DifferentiationTools()
        output = generate_all_outputs(cls.tool)
        cls.rows = output["rows"]
        cls.freefall_result = output["freefall_result"]

    def test_all_methods_meet_tolerance(self):
        failing_rows = [row for row in self.rows if not row["passed"]]
        self.assertEqual([], failing_rows)

    def test_gravity_from_interpolated_freefall_data(self):
        self.assertAlmostEqual(
            abs(self.freefall_result["estimated_accel_signed"]),
            9.81,
            delta=FREEFALL_GRAVITY_TOL,
        )

    def test_required_outputs_exist(self):
        required = [
            PROJECT_ROOT / "unit03" / "results" / "article_results" / "differentiation_test_results.csv",
            PROJECT_ROOT / "unit03" / "results" / "article_results" / "differentiation_test_results.json",
            PROJECT_ROOT / "unit03" / "results" / "article_results" / "differentiation_test_results.md",
            PROJECT_ROOT / "unit03" / "results" / "article_results" / "differentiation_summary.csv",
            PROJECT_ROOT / "unit03" / "results" / "article_results" / "differentiation_summary.json",
            PROJECT_ROOT / "unit03" / "results" / "article_results" / "differentiation_summary.md",
            PROJECT_ROOT / "unit03" / "results" / "article_results" / "differentiation_error_ranking.csv",
            PROJECT_ROOT / "unit03" / "results" / "article_results" / "differentiation_freefall_coefficients.csv",
            PROJECT_ROOT / "unit03" / "results" / "article_results" / "freefall_gravity_results.csv",
            PROJECT_ROOT / "unit03" / "results" / "article_results" / "freefall_gravity_results.json",
            PROJECT_ROOT / "unit03" / "results" / "article_results" / "freefall_gravity_results.md",
            PROJECT_ROOT / "unit03" / "results" / "article_results" / "run_metadata.json",
            PROJECT_ROOT / "unit03" / "results" / "article_results" / "unittest_report.txt",
            PROJECT_ROOT / "unit03" / "results" / "plots" / "sine_at_pi_over_4_error_vs_h.png",
            PROJECT_ROOT / "unit03" / "results" / "plots" / "sine_at_pi_over_4_error_vs_h.svg",
            PROJECT_ROOT / "unit03" / "results" / "plots" / "exp_at_0p3_error_vs_h.png",
            PROJECT_ROOT / "unit03" / "results" / "plots" / "exp_at_0p3_error_vs_h.svg",
            PROJECT_ROOT / "unit03" / "results" / "plots" / "poly_cubic_minus_quadratic_error_vs_h.png",
            PROJECT_ROOT / "unit03" / "results" / "plots" / "poly_cubic_minus_quadratic_error_vs_h.svg",
            PROJECT_ROOT / "unit03" / "results" / "plots" / "freefall_gravity_interpolation.png",
            PROJECT_ROOT / "unit03" / "results" / "plots" / "freefall_gravity_interpolation.svg",
            PROJECT_ROOT / "unit03" / "results" / "article_images" / "all_results_table.png",
            PROJECT_ROOT / "unit03" / "results" / "article_images" / "all_results_table.svg",
            PROJECT_ROOT / "unit03" / "results" / "article_images" / "summary_table.png",
            PROJECT_ROOT / "unit03" / "results" / "article_images" / "summary_table.svg",
            PROJECT_ROOT / "unit03" / "results" / "article_images" / "error_ranking_table.png",
            PROJECT_ROOT / "unit03" / "results" / "article_images" / "error_ranking_table.svg",
            PROJECT_ROOT / "unit03" / "results" / "article_images" / "sine_at_pi_over_4_results_table.png",
            PROJECT_ROOT / "unit03" / "results" / "article_images" / "sine_at_pi_over_4_results_table.svg",
            PROJECT_ROOT / "unit03" / "results" / "article_images" / "exp_at_0p3_results_table.png",
            PROJECT_ROOT / "unit03" / "results" / "article_images" / "exp_at_0p3_results_table.svg",
            PROJECT_ROOT / "unit03" / "results" / "article_images" / "poly_cubic_minus_quadratic_results_table.png",
            PROJECT_ROOT / "unit03" / "results" / "article_images" / "poly_cubic_minus_quadratic_results_table.svg",
            PROJECT_ROOT / "unit03" / "results" / "article_images" / "freefall_gravity_results_table.png",
            PROJECT_ROOT / "unit03" / "results" / "article_images" / "freefall_gravity_results_table.svg",
            PROJECT_ROOT / "unit03" / "results" / "article_images" / "freefall_source_data_table.png",
            PROJECT_ROOT / "unit03" / "results" / "article_images" / "freefall_source_data_table.svg",
        ]
        missing = [str(path) for path in required if not path.exists()]
        self.assertEqual([], missing)


if __name__ == "__main__":
    unittest.main(verbosity=2)
