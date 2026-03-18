"""Numerical result collection helpers for Unit 03 differentiation."""

from __future__ import annotations

from typing import Dict, List, Sequence

import numpy as np

from .config import (
    FREEFALL_GRAVITY_TOL,
    FREEFALL_POSITION_DATA,
    FREEFALL_TIME_DATA,
    METHODS,
    TEST_CASES,
)


def build_freefall_position_interpolant():
    """Return a quadratic position interpolant and the source arrays."""
    coeffs = np.polyfit(FREEFALL_TIME_DATA, FREEFALL_POSITION_DATA, 2)
    position_poly = np.poly1d(coeffs)
    return position_poly, FREEFALL_TIME_DATA.copy(), FREEFALL_POSITION_DATA.copy()


def estimate_gravity_from_interpolated_freefall(tool, h: float = 1e-5) -> Dict[str, object]:
    """Estimate gravitational acceleration by differentiating the interpolant twice."""
    position_poly, time_data, position_data = build_freefall_position_interpolant()

    def velocity(t):
        return tool.numerical_differentiation_3point(position_poly, t, h=h, method="central")

    def acceleration(t):
        return tool.numerical_differentiation_3point(velocity, t, h=h, method="central")

    t0 = float(time_data[len(time_data) // 2])
    accel_est = float(acceleration(t0))
    accel_mag = abs(accel_est)
    target_g = 9.81
    abs_error = abs(accel_mag - target_g)
    passed = abs_error <= FREEFALL_GRAVITY_TOL

    return {
        "case_name": "freefall_gravity_interpolation",
        "display_name": "Free-fall gravity from quadratic interpolant",
        "interpolant_type": "quadratic (polyfit degree 2)",
        "position_units": "m",
        "time_units": "s",
        "acceleration_units": "m/s^2",
        "evaluation_time": t0,
        "step_size": float(h),
        "accel_estimate_signed": accel_est,
        "accel_estimate_magnitude": accel_mag,
        "target_gravity_magnitude": target_g,
        "magnitude_abs_error": abs_error,
        "tolerance": float(FREEFALL_GRAVITY_TOL),
        "passed": bool(passed),
        "source_time_data": time_data.tolist(),
        "source_position_data": position_data.tolist(),
        "quadratic_coefficients": position_poly.c.tolist(),
    }


def collect_results(tool) -> List[Dict[str, object]]:
    """Collect analytic test results for all cases and methods."""
    rows: List[Dict[str, object]] = []

    for case in TEST_CASES:
        x = float(case["x"])
        h = float(case["h"])
        exact = float(case["df"](x))

        for method in METHODS:
            approx = float(tool.numerical_differentiation_3point(case["f"], x, h=h, method=method))
            abs_error = abs(approx - exact)
            rel_error = abs_error / max(abs(exact), np.finfo(float).eps)
            tol = float(case["tolerances"][method])

            rows.append(
                {
                    "case_name": case["name"],
                    "display_name": case["display_name"],
                    "method": method,
                    "x": x,
                    "h": h,
                    "exact": exact,
                    "approx": approx,
                    "abs_error": abs_error,
                    "rel_error": rel_error,
                    "tolerance": tol,
                    "passed": abs_error <= tol,
                }
            )

    return rows


def build_summary(rows: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    """Summarize analytic errors grouped by method."""
    summary: List[Dict[str, object]] = []

    for method in METHODS:
        method_rows = [row for row in rows if row["method"] == method]
        abs_errors = np.array([row["abs_error"] for row in method_rows], dtype=float)
        rel_errors = np.array([row["rel_error"] for row in method_rows], dtype=float)

        summary.append(
            {
                "method": method,
                "num_cases": len(method_rows),
                "all_passed": all(row["passed"] for row in method_rows),
                "max_abs_error": float(abs_errors.max()) if len(abs_errors) else float("nan"),
                "mean_abs_error": float(abs_errors.mean()) if len(abs_errors) else float("nan"),
                "max_rel_error": float(rel_errors.max()) if len(rel_errors) else float("nan"),
                "mean_rel_error": float(rel_errors.mean()) if len(rel_errors) else float("nan"),
            }
        )

    return summary


__all__ = [
    "build_freefall_position_interpolant",
    "estimate_gravity_from_interpolated_freefall",
    "collect_results",
    "build_summary",
]
