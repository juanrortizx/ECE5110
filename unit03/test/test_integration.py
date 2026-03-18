"""Unit tests and artifact generation for Unit 03 integration workflows."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lib.integration_tools import IntegrationTools
from unit03.integration.config import METHODS, MIN_OBSERVED_ORDER, UNIT_RESULTS_DIR
from unit03.integration.workflow import generate_all_outputs


class TestIntegrationMethods(unittest.TestCase):
    """Validate trapezoidal and Simpson workflows, including convergence."""

    @classmethod
    def setUpClass(cls):
        cls.tool = IntegrationTools()
        cls.workflow_output = generate_all_outputs(cls.tool)
        cls.methods_payload = cls.workflow_output["methods"]

    def test_trapezoidal_validation(self):
        with self.assertRaises(TypeError):
            self.tool.composite_trapezoidal(None, 0.0, 1.0, 10)
        with self.assertRaises(ValueError):
            self.tool.composite_trapezoidal(lambda x: x, 0.0, 1.0, 0)
        with self.assertRaises(ValueError):
            self.tool.composite_trapezoidal(lambda x: x, 1.0, 1.0, 10)

    def test_simpson_rejects_odd_subintervals(self):
        with self.assertRaises(ValueError):
            self.tool.composite_simpson(lambda x: x, 0.0, 1.0, 3)

    def test_observed_orders(self):
        for method in METHODS:
            for row in self.methods_payload[method]["summary_rows"]:
                self.assertGreaterEqual(
                    row["observed_order"],
                    MIN_OBSERVED_ORDER[method],
                    msg=(
                        f"Observed order too low for {method} / {row['case']}: "
                        f"{row['observed_order']} < {MIN_OBSERVED_ORDER[method]}"
                    ),
                )

    def test_required_outputs_exist(self):
        required = [
            UNIT_RESULTS_DIR / "article_results" / "integration_trapezoidal_results.csv",
            UNIT_RESULTS_DIR / "article_results" / "integration_simpson_results.csv",
            UNIT_RESULTS_DIR / "article_results" / "integration_unittest_report.txt",
            UNIT_RESULTS_DIR / "plots" / "integration_trapezoidal_error_vs_h.png",
            UNIT_RESULTS_DIR / "plots" / "integration_simpson_error_vs_h.png",
            UNIT_RESULTS_DIR / "article_images" / "integration_trapezoidal_summary_table.png",
            UNIT_RESULTS_DIR / "article_images" / "integration_simpson_summary_table.png",
        ]
        missing = [str(path) for path in required if not path.exists()]
        self.assertFalse(missing, msg=f"Missing expected output files: {missing}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
