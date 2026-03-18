"""Numerical calculators for Unit 03 differentiation workflow."""

import numpy as np

from .config import (
    FREEFALL_GRAVITY_TOL,
    FREEFALL_POSITION_DATA,
    FREEFALL_TIME_DATA,
    METHODS,
    TEST_CASES,
)


def build_freefall_position_interpolant():
    """Fit a quadratic position(t) interpolant for the free-fall dataset."""
    coeffs = np.polyfit(FREEFALL_TIME_DATA, FREEFALL_POSITION_DATA, 2)
    return coeffs, np.poly1d(coeffs)


def estimate_gravity_from_interpolated_freefall(tool, h):
    """Estimate gravitational acceleration by differentiating interpolated data twice."""
    coeffs, position_poly = build_freefall_position_interpolant()
    t0 = float(FREEFALL_TIME_DATA[len(FREEFALL_TIME_DATA) // 2])

    velocity = lambda t: tool.numerical_differentiation_3point(
        position_poly,
        t,
        h=h,
        method="central",
    )
    acceleration_est = float(
        tool.numerical_differentiation_3point(velocity, t0, h=h, method="central")
    )
    abs_accel = abs(acceleration_est)
    abs_error = abs(abs_accel - 9.81)

    return {
        "method": "central",
        "h": float(h),
        "evaluation_time": t0,
        "acceleration_signed": acceleration_est,
        "acceleration_magnitude": abs_accel,
        "target_gravity_magnitude": 9.81,
        "magnitude_abs_error": abs_error,
        "tolerance": float(FREEFALL_GRAVITY_TOL),
        "pass": bool(abs_error <= FREEFALL_GRAVITY_TOL),
        "poly_coefficients": [float(c) for c in coeffs.tolist()],
        "source_time_data": [float(v) for v in FREEFALL_TIME_DATA.tolist()],
        "source_position_data": [float(v) for v in FREEFALL_POSITION_DATA.tolist()],
    }


def collect_results(tool):
    """Evaluate all analytic differentiation test cases and methods."""
    rows = []
    for case in TEST_CASES:
        exact = float(case["df"](case["x"]))
        for method in METHODS:
            approx = float(
                tool.numerical_differentiation_3point(
                    case["f"],
                    case["x"],
                    h=case["h"],
                    method=method,
                )
            )
            abs_error = abs(approx - exact)
            rel_error = abs_error / abs(exact) if exact != 0.0 else np.nan
            tol = float(case["tolerances"][method])

            rows.append(
                {
                    "case_name": case["name"],
                    "case_display_name": case["display_name"],
                    "x": float(case["x"]),
                    "h": float(case["h"]),
                    "method": method,
                    "exact": exact,
                    "approx": approx,
                    "abs_error": float(abs_error),
                    "rel_error": float(rel_error),
                    "tolerance": tol,
                    "pass": bool(abs_error <= tol),
                }
            )
    return rows


def build_summary(rows):
    """Build per-method summary statistics from analytic result rows."""
    summary_rows = []
    for method in METHODS:
        method_rows = [row for row in rows if row["method"] == method]
        abs_errors = np.array([row["abs_error"] for row in method_rows], dtype=float)
        rel_errors = np.array([row["rel_error"] for row in method_rows], dtype=float)
        finite_rel = rel_errors[np.isfinite(rel_errors)]
        pass_count = sum(1 for row in method_rows if row["pass"])

        summary_rows.append(
            {
                "method": method,
                "num_cases": len(method_rows),
                "pass_count": pass_count,
                "fail_count": len(method_rows) - pass_count,
                "max_abs_error": float(np.max(abs_errors)) if len(abs_errors) else np.nan,
                "mean_abs_error": float(np.mean(abs_errors)) if len(abs_errors) else np.nan,
                "max_rel_error": (
                    float(np.max(finite_rel)) if len(finite_rel) else np.nan
                ),
                "mean_rel_error": (
                    float(np.mean(finite_rel)) if len(finite_rel) else np.nan
                ),
                "all_pass": bool(pass_count == len(method_rows)),
            }
        )

    return summary_rows
