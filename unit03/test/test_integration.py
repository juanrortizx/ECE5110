"""Unittest harness for Unit 03 integration workflow."""

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lib.integration_tools import IntegrationTools
from unit03.integration.config import (
    MIN_ORDER_SIMPSON,
    MIN_ORDER_TRAPEZOIDAL,
)
from unit03.integration.workflow import generate_all_outputs


class TestIntegrationMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool = IntegrationTools()
        cls.output = generate_all_outputs(cls.tool)

    def test_trapezoidal_validation_checks(self):
        with self.assertRaises(TypeError):
            self.tool.composite_trapezoidal(None, 0.0, 1.0, 4)
        with self.assertRaises(ValueError):
            self.tool.composite_trapezoidal(lambda x: x, 0.0, 1.0, 0)
        with self.assertRaises(ValueError):
            self.tool.composite_trapezoidal(lambda x: x, 1.0, 1.0, 4)

    def test_simpson_odd_n_rejected(self):
        with self.assertRaises(ValueError):
            self.tool.composite_simpson(lambda x: x**2, 0.0, 1.0, 5)

    def test_observed_orders(self):
        trap_summary = self.output["trapezoidal"]["summary"]
        simp_summary = self.output["simpson"]["summary"]

        for row in trap_summary:
            self.assertGreaterEqual(row["observed_order"], MIN_ORDER_TRAPEZOIDAL)

        for row in simp_summary:
            self.assertGreaterEqual(row["observed_order"], MIN_ORDER_SIMPSON)

    def test_required_outputs_exist(self):
        required = [
            PROJECT_ROOT / "unit03" / "results" / "article_results" / "integration_trapezoidal_results.csv",
            PROJECT_ROOT / "unit03" / "results" / "article_results" / "integration_trapezoidal_results.json",
            PROJECT_ROOT / "unit03" / "results" / "article_results" / "integration_trapezoidal_results.md",
            PROJECT_ROOT / "unit03" / "results" / "article_results" / "integration_trapezoidal_summary.csv",
            PROJECT_ROOT / "unit03" / "results" / "article_results" / "integration_trapezoidal_summary.json",
            PROJECT_ROOT / "unit03" / "results" / "article_results" / "integration_trapezoidal_summary.md",
            PROJECT_ROOT / "unit03" / "results" / "article_results" / "integration_trapezoidal_metadata.json",
            PROJECT_ROOT / "unit03" / "results" / "article_results" / "integration_simpson_results.csv",
            PROJECT_ROOT / "unit03" / "results" / "article_results" / "integration_simpson_results.json",
            PROJECT_ROOT / "unit03" / "results" / "article_results" / "integration_simpson_results.md",
            PROJECT_ROOT / "unit03" / "results" / "article_results" / "integration_simpson_summary.csv",
            PROJECT_ROOT / "unit03" / "results" / "article_results" / "integration_simpson_summary.json",
            PROJECT_ROOT / "unit03" / "results" / "article_results" / "integration_simpson_summary.md",
            PROJECT_ROOT / "unit03" / "results" / "article_results" / "integration_simpson_metadata.json",
            PROJECT_ROOT / "unit03" / "results" / "article_results" / "integration_unittest_report.txt",
            PROJECT_ROOT / "unit03" / "results" / "plots" / "integration_trapezoidal_error_vs_h.png",
            PROJECT_ROOT / "unit03" / "results" / "plots" / "integration_trapezoidal_error_vs_h.svg",
            PROJECT_ROOT / "unit03" / "results" / "plots" / "integration_simpson_error_vs_h.png",
            PROJECT_ROOT / "unit03" / "results" / "plots" / "integration_simpson_error_vs_h.svg",
            PROJECT_ROOT / "unit03" / "results" / "article_images" / "integration_trapezoidal_results_table.png",
            PROJECT_ROOT / "unit03" / "results" / "article_images" / "integration_trapezoidal_results_table.svg",
            PROJECT_ROOT / "unit03" / "results" / "article_images" / "integration_trapezoidal_summary_table.png",
            PROJECT_ROOT / "unit03" / "results" / "article_images" / "integration_trapezoidal_summary_table.svg",
            PROJECT_ROOT / "unit03" / "results" / "article_images" / "integration_simpson_results_table.png",
            PROJECT_ROOT / "unit03" / "results" / "article_images" / "integration_simpson_results_table.svg",
            PROJECT_ROOT / "unit03" / "results" / "article_images" / "integration_simpson_summary_table.png",
            PROJECT_ROOT / "unit03" / "results" / "article_images" / "integration_simpson_summary_table.svg",
        ]
        missing = [str(path) for path in required if not path.exists()]
        self.assertEqual([], missing)


if __name__ == "__main__":
    unittest.main(verbosity=2)
