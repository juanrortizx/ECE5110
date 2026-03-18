"""Numerical calculators for Unit 03 integration workflows."""

from __future__ import annotations

import numpy as np

from unit03.integration.config import BENCHMARK_CASES, METHOD_TOOL_MAP, N_VALUES


def collect_method_results(tool, method):
    """Collect benchmark integration rows for one method."""
    rows = []
    method_name = METHOD_TOOL_MAP[method]
    integrate = getattr(tool, method_name)

    for case in BENCHMARK_CASES:
        exact = float(case["exact"])
        for n in N_VALUES:
            approx = float(integrate(case["f"], case["a"], case["b"], n))
            abs_error = abs(approx - exact)
            rel_error = abs_error / max(abs(exact), 1e-15)
            h = abs((case["b"] - case["a"]) / float(n))
            rows.append(
                {
                    "method": method,
                    "case": case["name"],
                    "case_display": case["display_name"],
                    "a": float(case["a"]),
                    "b": float(case["b"]),
                    "n": int(n),
                    "h": h,
                    "exact": exact,
                    "approx": approx,
                    "abs_error": abs_error,
                    "rel_error": rel_error,
                }
            )
    return rows


def observed_order(errors, hs):
    """Estimate convergence order from log(error)-log(h) slope."""
    errors = np.asarray(errors, dtype=float)
    hs = np.asarray(hs, dtype=float)

    # If all sampled errors are exactly zero, the method is exact on this case.
    if np.all(errors == 0.0):
        return float("inf")

    mask = (errors > 0.0) & (hs > 0.0)
    if np.count_nonzero(mask) < 2:
        return float("nan")
    slope, _ = np.polyfit(np.log(hs[mask]), np.log(errors[mask]), 1)
    return float(slope)


def build_summary(rows):
    """Build per-case summary rows with observed convergence order."""
    summary_rows = []
    case_names = sorted({row["case"] for row in rows})
    for case_name in case_names:
        case_rows = sorted(
            [row for row in rows if row["case"] == case_name],
            key=lambda row: row["n"],
        )
        errors = [row["abs_error"] for row in case_rows]
        hs = [row["h"] for row in case_rows]
        best_row = min(case_rows, key=lambda row: row["abs_error"])
        summary_rows.append(
            {
                "method": case_rows[0]["method"],
                "case": case_name,
                "case_display": case_rows[0]["case_display"],
                "observed_order": observed_order(errors, hs),
                "best_n": int(best_row["n"]),
                "best_abs_error": float(best_row["abs_error"]),
                "final_n": int(case_rows[-1]["n"]),
                "final_abs_error": float(case_rows[-1]["abs_error"]),
            }
        )
    return summary_rows
