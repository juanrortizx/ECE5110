"""Numerical and derived calculations for Unit 03 differentiation outputs."""

import numpy as np

from unit03.differentiation.config import (
    FREEFALL_GRAVITY_TOL,
    FREEFALL_POSITION_DATA,
    FREEFALL_TIME_DATA,
    METHODS,
    TEST_CASES,
)


def build_freefall_position_interpolant():
    coeffs = np.polyfit(FREEFALL_TIME_DATA, FREEFALL_POSITION_DATA, 2)
    return np.poly1d(coeffs), coeffs


def estimate_gravity_from_interpolated_freefall(tool, h=1e-5):
    position_poly, coeffs = build_freefall_position_interpolant()
    t0 = float(FREEFALL_TIME_DATA[len(FREEFALL_TIME_DATA) // 2])

    def velocity_fn(t):
        return tool.numerical_differentiation_3point(position_poly, t, h=h, method="central")

    accel_est = tool.numerical_differentiation_3point(velocity_fn, t0, h=h, method="central")
    abs_g = abs(accel_est)
    abs_err = abs(abs_g - 9.81)

    return {
        "step_size": float(h),
        "evaluation_time": t0,
        "estimated_accel_signed": float(accel_est),
        "estimated_accel_magnitude": float(abs_g),
        "target_gravity_magnitude": 9.81,
        "magnitude_abs_error": float(abs_err),
        "tolerance": float(FREEFALL_GRAVITY_TOL),
        "passed": bool(abs_err <= FREEFALL_GRAVITY_TOL),
        "position_data": FREEFALL_POSITION_DATA.tolist(),
        "time_data": FREEFALL_TIME_DATA.tolist(),
        "poly_coefficients": [float(value) for value in coeffs.tolist()],
    }


def collect_results(tool):
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
            rel_error = abs_error / abs(exact) if exact != 0 else 0.0
            tol = float(case["tolerances"][method])
            rows.append(
                {
                    "case_name": case["name"],
                    "case_display": case["display_name"],
                    "method": method,
                    "x": float(case["x"]),
                    "h": float(case["h"]),
                    "exact": exact,
                    "approx": approx,
                    "abs_error": float(abs_error),
                    "rel_error": float(rel_error),
                    "tolerance": tol,
                    "passed": bool(abs_error <= tol),
                }
            )
    return rows


def build_summary(rows):
    summary_rows = []
    for method in METHODS:
        method_rows = [row for row in rows if row["method"] == method]
        abs_errors = np.array([row["abs_error"] for row in method_rows], dtype=float)
        rel_errors = np.array([row["rel_error"] for row in method_rows], dtype=float)
        pass_count = sum(1 for row in method_rows if row["passed"])
        summary_rows.append(
            {
                "method": method,
                "total_cases": int(len(method_rows)),
                "pass_count": int(pass_count),
                "fail_count": int(len(method_rows) - pass_count),
                "max_abs_error": float(np.max(abs_errors)) if len(abs_errors) else 0.0,
                "mean_abs_error": float(np.mean(abs_errors)) if len(abs_errors) else 0.0,
                "max_rel_error": float(np.max(rel_errors)) if len(rel_errors) else 0.0,
                "mean_rel_error": float(np.mean(rel_errors)) if len(rel_errors) else 0.0,
            }
        )
    return summary_rows
