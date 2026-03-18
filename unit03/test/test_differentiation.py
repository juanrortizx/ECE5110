"""Unit tests and artifact generator for Unit 03 differentiation workflow."""

import csv
import json
import shutil
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lib.differentiation_tools import DifferentiationTools
from unit03.differentiation.config import (
    FREEFALL_GRAVITY_TOL,
    FREEFALL_POSITION_DATA,
    FREEFALL_TIME_DATA,
    H_VALUES,
    METHODS,
    TEST_CASES,
    UNIT_RESULTS_DIR,
)
from unit03.differentiation.workflow import generate_all_outputs


class TestDifferentiationThreePoint(unittest.TestCase):
    """Validates 3-point differentiation methods and output artifacts."""

    @classmethod
    def setUpClass(cls):
        cls.tool = DifferentiationTools()
        cls.workflow = generate_all_outputs(cls.tool)
        cls.rows = cls.workflow["rows"]
        cls.freefall_result = cls.workflow["freefall_result"]

    def test_all_methods_meet_tolerance(self):
        failing_rows = [
            row
            for row in self.rows
            if not row["pass"]
        ]
        details = [
            (
                f"{row['case_name']}::{row['method']} abs_error={row['abs_error']:.6e} "
                f"tol={row['tolerance']:.6e}"
            )
            for row in failing_rows
        ]
        self.assertFalse(failing_rows, msg="\n".join(details))

    def test_gravity_from_interpolated_freefall_data(self):
        accel_est = float(self.freefall_result["acceleration_signed"])
        self.assertAlmostEqual(abs(accel_est), 9.81, delta=FREEFALL_GRAVITY_TOL)

    def test_invalid_method_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.tool.numerical_differentiation_3point(np.sin, 0.5, h=1e-4, method="invalid")

    def test_nonpositive_h_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.tool.numerical_differentiation_3point(np.sin, 0.5, h=0.0, method="central")


if __name__ == "__main__":
    unittest.main(verbosity=2)
