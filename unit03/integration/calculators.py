"""Numerical sweep helpers for Unit 03 integration."""

from __future__ import annotations

from typing import Dict, List, Sequence

import numpy as np

from .config import BENCHMARK_CASES, N_VALUES


def collect_method_results(tool, method_name: str, method_callable) -> List[Dict[str, object]]:
    """Collect per-case, per-n integration approximations for a method."""
    rows: List[Dict[str, object]] = []

    for case in BENCHMARK_CASES:
        for n in N_VALUES:
            approx = float(method_callable(case["f"], case["a"], case["b"], n))
            h = (case["b"] - case["a"]) / float(n)
            abs_error = abs(approx - float(case["exact"]))

            rows.append(
                {
                    "case_name": case["case_name"],
                    "display_name": case["display_name"],
                    "method": method_name,
                    "a": float(case["a"]),
                    "b": float(case["b"]),
                    "n": int(n),
                    "h": h,
                    "exact": float(case["exact"]),
                    "approx": approx,
                    "abs_error": abs_error,
                }
            )

    return rows


def observed_order(rows: Sequence[Dict[str, object]]) -> float:
    """Estimate the observed convergence rate using log-log slope."""
    h_values = np.array([row["h"] for row in rows], dtype=float)
    error_values = np.array([row["abs_error"] for row in rows], dtype=float)

    valid = np.isfinite(error_values) & (error_values > 1.0e-15)
    if np.count_nonzero(valid) >= 3:
        h_values = h_values[valid]
        error_values = error_values[valid]
    else:
        if np.all(error_values <= 1.0e-15):
            return float("inf")
        positive = error_values > 0.0
        if np.count_nonzero(positive) >= 3:
            h_values = h_values[positive]
            error_values = error_values[positive]
        else:
            error_values = np.maximum(error_values, np.finfo(float).tiny)

    slope, _ = np.polyfit(np.log(h_values), np.log(error_values), 1)
    return float(slope)


def build_summary(rows: Sequence[Dict[str, object]], expected_order: float, tol_key: str):
    """Summarize integration results for tolerance assertions."""
    summary_rows: List[Dict[str, object]] = []

    for case in BENCHMARK_CASES:
        case_rows = [row for row in rows if row["case_name"] == case["case_name"]]
        finest_row = min(case_rows, key=lambda row: row["h"])
        final_tol = float(case[tol_key])

        summary_rows.append(
            {
                "method": finest_row["method"],
                "case_name": case["case_name"],
                "display_name": case["display_name"],
                "n_values": ",".join(str(row["n"]) for row in case_rows),
                "num_runs": len(case_rows),
                "expected_order": expected_order,
                "observed_order": observed_order(case_rows),
                "finest_n": int(finest_row["n"]),
                "finest_h": float(finest_row["h"]),
                "finest_approx": float(finest_row["approx"]),
                "exact": float(case["exact"]),
                "finest_abs_error": float(finest_row["abs_error"]),
                "final_tolerance": final_tol,
                "passed_final_tolerance": float(finest_row["abs_error"]) <= final_tol,
            }
        )

    return summary_rows


__all__ = ["collect_method_results", "observed_order", "build_summary"]
