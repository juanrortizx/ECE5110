"""Unit tests and artifact generation for Unit 03 3-point differentiation."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lib.differentiation_tools import DifferentiationTools
from unit03.differentiation.config import (
    FREEFALL_GRAVITY_TOL,
    METHODS,
    TEST_CASES,
    UNIT_RESULTS_DIR,
)
from unit03.differentiation.workflow import generate_all_outputs


class TestDifferentiationThreePoint(unittest.TestCase):
    """Validate 3-point differentiation accuracy and gravity estimate outputs."""

    @classmethod
    def setUpClass(cls):
        cls.tool = DifferentiationTools()
        cls.workflow_output = generate_all_outputs(cls.tool)
        cls.rows = cls.workflow_output["rows"]
        cls.freefall_result = cls.workflow_output["freefall_result"]

    def test_all_methods_meet_tolerance(self):
        failures = [
            row
            for row in self.rows
            if not row["passed"]
            or row["method"] not in METHODS
            or row["case"] not in {case["name"] for case in TEST_CASES}
        ]
        self.assertFalse(
            failures,
            msg=f"Differentiation tolerance failures detected: {failures}",
        )

    def test_gravity_from_interpolated_freefall_data(self):
        accel_est = float(self.freefall_result["acceleration_signed"])
        self.assertAlmostEqual(abs(accel_est), 9.81, delta=FREEFALL_GRAVITY_TOL)

    def test_required_outputs_exist(self):
        required = [
            UNIT_RESULTS_DIR / "article_results" / "differentiation_test_results.csv",
            UNIT_RESULTS_DIR / "article_results" / "differentiation_summary.csv",
            UNIT_RESULTS_DIR / "article_results" / "run_metadata.json",
            UNIT_RESULTS_DIR / "article_results" / "freefall_gravity_results.json",
            UNIT_RESULTS_DIR / "article_results" / "unittest_report.txt",
            UNIT_RESULTS_DIR / "plots" / "freefall_gravity_interpolation.png",
            UNIT_RESULTS_DIR / "article_images" / "summary_table.png",
        ]
        missing = [str(path) for path in required if not path.exists()]
        self.assertFalse(missing, msg=f"Missing expected output files: {missing}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
