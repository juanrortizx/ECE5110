"""Plot and table-image generation for Unit 03 differentiation workflow."""

import numpy as np
import matplotlib.pyplot as plt

from unit03.common.table_images import render_table_dual_format
from unit03.differentiation.config import H_VALUES, METHODS, TEST_CASES


def _format_rows(rows, keys):
    formatted = []
    for row in rows:
        formatted_row = {}
        for key in keys:
            value = row.get(key)
            if isinstance(value, float):
                formatted_row[key] = f"{value:.6e}"
            else:
                formatted_row[key] = str(value)
        formatted.append(formatted_row)
    return formatted


def generate_article_images(rows, article_images_dir, freefall_result):
    summary_rows = []
    for method in METHODS:
        subset = [row for row in rows if row["method"] == method]
        summary_rows.append(
            {
                "method": method,
                "count": len(subset),
                "pass_count": sum(1 for row in subset if row["passed"]),
                "max_abs_error": max(row["abs_error"] for row in subset),
                "mean_abs_error": float(np.mean([row["abs_error"] for row in subset])),
            }
        )

    render_table_dual_format(
        _format_rows(rows, ["case_name", "method", "exact", "approx", "abs_error", "tolerance", "passed"]),
        ["case_name", "method", "exact", "approx", "abs_error", "tolerance", "passed"],
        article_images_dir / "all_results_table",
        title="Differentiation Results",
    )

    render_table_dual_format(
        _format_rows(summary_rows, ["method", "count", "pass_count", "max_abs_error", "mean_abs_error"]),
        ["method", "count", "pass_count", "max_abs_error", "mean_abs_error"],
        article_images_dir / "summary_table",
        title="Differentiation Summary",
    )

    ranking = sorted(rows, key=lambda row: row["abs_error"], reverse=True)
    render_table_dual_format(
        _format_rows(ranking, ["case_name", "method", "abs_error", "rel_error", "passed"]),
        ["case_name", "method", "abs_error", "rel_error", "passed"],
        article_images_dir / "error_ranking_table",
        title="Differentiation Error Ranking",
    )

    for case in TEST_CASES:
        case_rows = [row for row in rows if row["case_name"] == case["name"]]
        render_table_dual_format(
            _format_rows(case_rows, ["method", "exact", "approx", "abs_error", "tolerance", "passed"]),
            ["method", "exact", "approx", "abs_error", "tolerance", "passed"],
            article_images_dir / f"{case['name']}_results_table",
            title=case["display_name"],
        )

    freefall_table_rows = [
        {
            "evaluation_time": freefall_result["evaluation_time"],
            "signed_accel": freefall_result["estimated_accel_signed"],
            "abs_accel": freefall_result["estimated_accel_magnitude"],
            "target_abs_g": freefall_result["target_gravity_magnitude"],
            "abs_error": freefall_result["magnitude_abs_error"],
            "tolerance": freefall_result["tolerance"],
            "passed": freefall_result["passed"],
        }
    ]
    render_table_dual_format(
        _format_rows(
            freefall_table_rows,
            ["evaluation_time", "signed_accel", "abs_accel", "target_abs_g", "abs_error", "tolerance", "passed"],
        ),
        ["evaluation_time", "signed_accel", "abs_accel", "target_abs_g", "abs_error", "tolerance", "passed"],
        article_images_dir / "freefall_gravity_results_table",
        title="Free-Fall Gravity Estimate",
    )

    source_rows = []
    for t_value, s_value in zip(freefall_result["time_data"], freefall_result["position_data"]):
        source_rows.append({"time_s": t_value, "position_m": s_value})
    render_table_dual_format(
        _format_rows(source_rows, ["time_s", "position_m"]),
        ["time_s", "position_m"],
        article_images_dir / "freefall_source_data_table",
        title="Free-Fall Source Data",
    )


def generate_plots(tool, plots_dir, freefall_result):
    for case in TEST_CASES:
        exact = case["df"](case["x"])

        plt.figure(figsize=(7.2, 4.4))
        for method in METHODS:
            errors = []
            for h in H_VALUES:
                approx = tool.numerical_differentiation_3point(case["f"], case["x"], h=float(h), method=method)
                errors.append(abs(approx - exact))
            plt.loglog(H_VALUES, errors, label=method)

        plt.grid(True, which="both", ls="--", alpha=0.35)
        plt.xlabel("h")
        plt.ylabel("absolute error")
        plt.title(f"3-point differentiation error vs h: {case['display_name']}")
        plt.legend()
        plt.tight_layout()
        stem = plots_dir / f"{case['name']}_error_vs_h"
        plt.savefig(f"{stem}.png", dpi=220)
        plt.savefig(f"{stem}.svg")
        plt.close()

    coeffs = np.array(freefall_result["poly_coefficients"], dtype=float)
    poly = np.poly1d(coeffs)
    t_data = np.array(freefall_result["time_data"], dtype=float)
    y_data = np.array(freefall_result["position_data"], dtype=float)
    t_dense = np.linspace(np.min(t_data), np.max(t_data), 400)

    plt.figure(figsize=(7.2, 4.4))
    plt.scatter(t_data, y_data, label="source data", color="tab:blue")
    plt.plot(t_dense, poly(t_dense), label="quadratic interpolant", color="tab:orange")
    plt.axvline(freefall_result["evaluation_time"], color="tab:green", linestyle="--", label="evaluation time")
    plt.title("Free-fall interpolation and gravity estimate")
    plt.xlabel("time [s]")
    plt.ylabel("position [m]")
    plt.text(
        0.02,
        0.03,
        f"|g| est = {freefall_result['estimated_accel_magnitude']:.4f} m/s^2",
        transform=plt.gca().transAxes,
        fontsize=10,
        bbox={"facecolor": "white", "alpha": 0.7, "edgecolor": "none"},
    )
    plt.grid(True, ls="--", alpha=0.35)
    plt.legend()
    plt.tight_layout()
    stem = plots_dir / "freefall_gravity_interpolation"
    plt.savefig(f"{stem}.png", dpi=220)
    plt.savefig(f"{stem}.svg")
    plt.close()
