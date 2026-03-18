import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lib.differentiation_tools import DifferentiationTools
from unit03.differentiation import config
from unit03.differentiation.workflow import generate_all_outputs


class TestDifferentiationThreePoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool = DifferentiationTools()
        cls.generated = generate_all_outputs(cls.tool)
        cls.rows = cls.generated["rows"]
        cls.freefall_result = cls.generated["freefall_result"]

    def test_all_methods_meet_tolerance(self):
        failures = [row for row in self.rows if not row["passed"]]
        if failures:
            details = [
                (
                    f"case={row['case_name']}, method={row['method']}, "
                    f"abs_error={row['abs_error']:.6e}, tol={row['tolerance']:.6e}"
                )
                for row in failures
            ]
            self.fail("Analytic tolerance failures:\n" + "\n".join(details))

    def test_gravity_from_interpolated_freefall_data(self):
        accel_est = float(self.freefall_result["accel_estimate_signed"])
        self.assertAlmostEqual(abs(accel_est), 9.81, delta=config.FREEFALL_GRAVITY_TOL)

    def test_invalid_method_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.tool.numerical_differentiation_3point(config.TEST_CASES[0]["f"], 0.1, h=1e-5, method="invalid")

    def test_nonpositive_h_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.tool.numerical_differentiation_3point(config.TEST_CASES[0]["f"], 0.1, h=0.0, method="central")


if __name__ == "__main__":
    unittest.main(verbosity=2)
