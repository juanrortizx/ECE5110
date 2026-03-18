"""Numerical calculators for Unit 03 integration workflows."""

import numpy as np

from .config import BENCHMARK_CASES, N_VALUES


def collect_method_results(tool, method_key):
    """Collect per-case, per-n integration errors for a selected method."""
    if method_key == "trapezoidal":
        integrator = tool.composite_trapezoidal
    elif method_key == "simpson":
        integrator = tool.composite_simpson
    else:
        raise ValueError("method_key must be 'trapezoidal' or 'simpson'.")

    rows = []
    case_orders = {}

    for case in BENCHMARK_CASES:
        case_rows = []
        for n in N_VALUES:
            approx = float(integrator(case["f"], case["a"], case["b"], n))
            abs_error = abs(approx - case["exact"])
            h = (case["b"] - case["a"]) / float(n)
            row = {
                "method": method_key,
                "case_name": case["name"],
                "case_display_name": case["display_name"],
                "a": float(case["a"]),
                "b": float(case["b"]),
                "n": int(n),
                "h": float(h),
                "exact": float(case["exact"]),
                "approx": approx,
                "abs_error": float(abs_error),
            }
            rows.append(row)
            case_rows.append(row)

        case_orders[case["name"]] = observed_order(case_rows)

    return rows, case_orders


def observed_order(case_rows):
    """Estimate convergence order via linear fit of log(error) vs log(h)."""
    hs = np.array([row["h"] for row in case_rows], dtype=float)
    errors = np.array([row["abs_error"] for row in case_rows], dtype=float)

    if np.allclose(errors, 0.0):
        return float("inf")

    mask = (hs > 0.0) & (errors > 0.0)
    hs = hs[mask]
    errors = errors[mask]

    if hs.size < 3:
        return float("nan")

    slope, _ = np.polyfit(np.log(hs), np.log(errors), 1)
    return float(slope)


def build_summary(rows, case_orders, method_key, min_order):
    """Summarize best errors and observed orders for each benchmark case."""
    summary_rows = []
    for case in BENCHMARK_CASES:
        case_rows = [r for r in rows if r["case_name"] == case["name"]]
        best = min(case_rows, key=lambda r: r["n"])
        final = max(case_rows, key=lambda r: r["n"])
        summary_rows.append(
            {
                "method": method_key,
                "case_name": case["name"],
                "n_min": int(best["n"]),
                "n_max": int(final["n"]),
                "final_abs_error": float(final["abs_error"]),
                "min_abs_error": float(min(r["abs_error"] for r in case_rows)),
                "observed_order": float(case_orders[case["name"]]),
                "order_pass": bool(case_orders[case["name"]] >= min_order),
            }
        )
    return summary_rows
