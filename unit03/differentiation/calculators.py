"""Numerical result collectors for Unit 03 differentiation."""

from __future__ import annotations

import numpy as np

from unit03.differentiation.config import (
    FREEFALL_GRAVITY_TOL,
    FREEFALL_POSITION_DATA,
    FREEFALL_TIME_DATA,
    METHODS,
    TEST_CASES,
)


def build_freefall_position_interpolant():
    """Build quadratic interpolant for free-fall position data."""
    coeffs = np.polyfit(FREEFALL_TIME_DATA, FREEFALL_POSITION_DATA, 2)
    return np.poly1d(coeffs), coeffs


def estimate_gravity_from_interpolated_freefall(tool, h=1e-3):
    """Estimate gravitational acceleration via two numerical differentiations."""
    position_poly, coeffs = build_freefall_position_interpolant()
    t0 = float(FREEFALL_TIME_DATA[len(FREEFALL_TIME_DATA) // 2])

    velocity = lambda t: tool.numerical_differentiation_3point(
        position_poly, t, h=h, method="central"
    )
    accel_est = float(
        tool.numerical_differentiation_3point(velocity, t0, h=h, method="central")
    )
    accel_mag = abs(accel_est)
    abs_error = abs(accel_mag - 9.81)

    return {
        "step_size": h,
        "evaluation_time": t0,
        "acceleration_signed": accel_est,
        "acceleration_magnitude": accel_mag,
        "target_abs_gravity": 9.81,
        "absolute_error": abs_error,
        "tolerance": FREEFALL_GRAVITY_TOL,
        "passed": abs_error <= FREEFALL_GRAVITY_TOL,
        "coefficients": [float(v) for v in coeffs],
        "time_data": [float(v) for v in FREEFALL_TIME_DATA],
        "position_data": [float(v) for v in FREEFALL_POSITION_DATA],
    }


def collect_results(tool):
    """Collect derivative approximations for all analytic test cases."""
    rows = []
    for case in TEST_CASES:
        x0 = float(case["x"])
        exact = float(case["df"](x0))
        h = float(case["h"])
        for method in METHODS:
            approx = float(
                tool.numerical_differentiation_3point(case["f"], x0, h=h, method=method)
            )
            abs_error = abs(approx - exact)
            rel_error = abs_error / max(abs(exact), 1e-15)
            tolerance = float(case["tolerances"][method])
            rows.append(
                {
                    "case": case["name"],
                    "case_display": case["display_name"],
                    "method": method,
                    "x": x0,
                    "h": h,
                    "exact": exact,
                    "approx": approx,
                    "abs_error": abs_error,
                    "rel_error": rel_error,
                    "tolerance": tolerance,
                    "passed": abs_error <= tolerance,
                }
            )
    return rows


def build_summary(rows):
    """Aggregate pass/fail counts and error statistics by differentiation method."""
    summary_rows = []
    for method in METHODS:
        method_rows = [row for row in rows if row["method"] == method]
        abs_errors = np.array([row["abs_error"] for row in method_rows], dtype=float)
        rel_errors = np.array([row["rel_error"] for row in method_rows], dtype=float)
        passed = sum(1 for row in method_rows if row["passed"])
        total = len(method_rows)
        summary_rows.append(
            {
                "method": method,
                "passed": passed,
                "failed": total - passed,
                "total": total,
                "max_abs_error": float(abs_errors.max()) if total else 0.0,
                "mean_abs_error": float(abs_errors.mean()) if total else 0.0,
                "max_rel_error": float(rel_errors.max()) if total else 0.0,
                "mean_rel_error": float(rel_errors.mean()) if total else 0.0,
            }
        )
    return summary_rows
