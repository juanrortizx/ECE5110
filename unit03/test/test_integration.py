"""Unit tests and artifact generator for Unit 03 integration workflows."""

import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lib.integration_tools import IntegrationTools
from unit03.integration.config import BENCHMARK_CASES, MIN_OBSERVED_ORDERS
from unit03.integration.workflow import generate_all_outputs


class TestCompositeIntegrationMethods(unittest.TestCase):
    """Validates trapezoidal and Simpson integration workflow outputs."""

    @classmethod
    def setUpClass(cls):
        cls.tool = IntegrationTools()
        cls.workflow = generate_all_outputs(cls.tool)

    def test_trapezoidal_final_accuracy(self):
        rows = self.workflow["trapezoidal"]["rows"]
        for case in BENCHMARK_CASES:
            case_rows = [r for r in rows if r["case_name"] == case["name"]]
            final_row = max(case_rows, key=lambda r: r["n"])
            self.assertLessEqual(final_row["abs_error"], case["trapezoidal_tol"])

    def test_simpson_final_accuracy(self):
        rows = self.workflow["simpson"]["rows"]
        for case in BENCHMARK_CASES:
            case_rows = [r for r in rows if r["case_name"] == case["name"]]
            final_row = max(case_rows, key=lambda r: r["n"])
            self.assertLessEqual(final_row["abs_error"], case["simpson_tol"])

    def test_observed_orders(self):
        trap_orders = self.workflow["trapezoidal"]["case_orders"]
        simp_orders = self.workflow["simpson"]["case_orders"]

        for case_name, order in trap_orders.items():
            self.assertGreaterEqual(order, MIN_OBSERVED_ORDERS["trapezoidal"], msg=case_name)
        for case_name, order in simp_orders.items():
            self.assertGreaterEqual(order, MIN_OBSERVED_ORDERS["simpson"], msg=case_name)

    def test_simpson_requires_even_n(self):
        with self.assertRaises(ValueError):
            self.tool.composite_simpson(lambda x: x**2, 0.0, 1.0, 3)

    def test_trapezoidal_validation_errors(self):
        with self.assertRaises(TypeError):
            self.tool.composite_trapezoidal(1.23, 0.0, 1.0, 8)
        with self.assertRaises(ValueError):
            self.tool.composite_trapezoidal(lambda x: x, 0.0, 1.0, 0)
        with self.assertRaises(ValueError):
            self.tool.composite_trapezoidal(lambda x: x, 1.0, 1.0, 8)


if __name__ == "__main__":
    unittest.main(verbosity=2)
