"""Computation helpers for Unit 03 integration results and summaries."""

import numpy as np

from unit03.integration.config import BENCHMARK_CASES, N_VALUES


def collect_method_results(tool, method_key):
    if method_key == "trapezoidal":
        method = tool.composite_trapezoidal
    elif method_key == "simpson":
        method = tool.composite_simpson
    else:
        raise ValueError("Unknown method key")

    rows = []
    for case in BENCHMARK_CASES:
        for n in N_VALUES:
            approx = float(method(case["f"], case["a"], case["b"], n))
            abs_error = abs(approx - case["exact"])
            h = (case["b"] - case["a"]) / float(n)
            rows.append(
                {
                    "method": method_key,
                    "case_name": case["name"],
                    "case_display": case["display_name"],
                    "a": float(case["a"]),
                    "b": float(case["b"]),
                    "n": int(n),
                    "h": float(h),
                    "exact": float(case["exact"]),
                    "approx": approx,
                    "abs_error": float(abs_error),
                }
            )
    return rows


def observed_order(rows, case_name):
    all_case_rows = [row for row in rows if row["case_name"] == case_name]
    positive_rows = [row for row in all_case_rows if row["abs_error"] > 0]

    if len(all_case_rows) >= 2 and len(positive_rows) == 0:
        return float("inf")
    if len(positive_rows) < 2:
        return float("nan")

    case_rows = sorted(positive_rows, key=lambda row: row["h"], reverse=True)
    h_vals = np.array([row["h"] for row in case_rows], dtype=float)
    e_vals = np.array([row["abs_error"] for row in case_rows], dtype=float)

    slope, _ = np.polyfit(np.log(h_vals), np.log(e_vals), 1)
    return float(slope)


def build_summary(rows):
    summary_rows = []
    case_names = sorted({row["case_name"] for row in rows})
    for case_name in case_names:
        case_rows = [row for row in rows if row["case_name"] == case_name]
        case_rows = sorted(case_rows, key=lambda row: row["n"])
        abs_errors = np.array([row["abs_error"] for row in case_rows], dtype=float)
        summary_rows.append(
            {
                "method": case_rows[0]["method"],
                "case_name": case_name,
                "min_abs_error": float(np.min(abs_errors)),
                "max_abs_error": float(np.max(abs_errors)),
                "final_n": int(case_rows[-1]["n"]),
                "final_abs_error": float(case_rows[-1]["abs_error"]),
                "observed_order": observed_order(rows, case_name),
            }
        )
    return summary_rows
