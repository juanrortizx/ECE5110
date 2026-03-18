"""Plot and table-image generation for Unit 03 differentiation."""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from unit03.common.artifact_io import format_rows_for_columns
from unit03.common.table_images import render_table_image, save_figure_png_svg
from unit03.differentiation.artifacts import sanitize_filename
from unit03.differentiation.calculators import build_freefall_position_interpolant, build_summary
from unit03.differentiation.config import H_VALUES, METHODS, TEST_CASES


CASE_TABLE_STEM_BY_NAME = {
    "exp_x": "exp_at_0p3_results_table",
    "cubic_poly": "poly_cubic_minus_quadratic_results_table",
    "sin_x": "sine_at_pi_over_4_results_table",
}

CASE_PLOT_STEM_BY_NAME = {
    "exp_x": "exp_at_0p3_error_vs_h",
    "cubic_poly": "poly_cubic_minus_quadratic_error_vs_h",
    "sin_x": "sine_at_pi_over_4_error_vs_h",
}


def generate_article_images(rows, article_images_dir, freefall_result):
    """Render summary tables for article insertion."""
    summary_rows = build_summary(rows)
    ranking_rows = sorted(rows, key=lambda row: row["abs_error"], reverse=True)

    result_cols = [
        "case",
        "method",
        "x",
        "h",
        "exact",
        "approx",
        "abs_error",
        "tolerance",
        "passed",
    ]
    summary_cols = [
        "method",
        "passed",
        "failed",
        "max_abs_error",
        "mean_abs_error",
        "max_rel_error",
    ]

    render_table_image(
        format_rows_for_columns(rows, result_cols, float_sigfigs=8),
        result_cols,
        "Differentiation Results",
        article_images_dir / "all_results_table",
    )
    render_table_image(
        format_rows_for_columns(summary_rows, summary_cols, float_sigfigs=8),
        summary_cols,
        "Differentiation Summary",
        article_images_dir / "summary_table",
    )
    render_table_image(
        format_rows_for_columns(ranking_rows, result_cols, float_sigfigs=8),
        result_cols,
        "Differentiation Error Ranking",
        article_images_dir / "error_ranking_table",
    )

    for case in TEST_CASES:
        case_rows = [row for row in rows if row["case"] == case["name"]]
        render_table_image(
            format_rows_for_columns(case_rows, result_cols, float_sigfigs=8),
            result_cols,
            f"Differentiation Case: {case['display_name']}",
            article_images_dir / CASE_TABLE_STEM_BY_NAME.get(
                case["name"], f"differentiation_case_{sanitize_filename(case['name'])}_table"
            ),
        )

    freefall_rows = [
        {
            "step_size": freefall_result["step_size"],
            "evaluation_time": freefall_result["evaluation_time"],
            "accel_signed": freefall_result["acceleration_signed"],
            "accel_magnitude": freefall_result["acceleration_magnitude"],
            "target_abs_g": freefall_result["target_abs_gravity"],
            "abs_error": freefall_result["absolute_error"],
            "tolerance": freefall_result["tolerance"],
            "passed": freefall_result["passed"],
        }
    ]
    freefall_cols = list(freefall_rows[0].keys())
    render_table_image(
        format_rows_for_columns(freefall_rows, freefall_cols, float_sigfigs=8),
        freefall_cols,
        "Free-Fall Gravity Estimate",
        article_images_dir / "freefall_gravity_results_table",
    )

    sample_rows = [
        {"time": t, "position": x}
        for t, x in zip(freefall_result["time_data"], freefall_result["position_data"])
    ]
    render_table_image(
        format_rows_for_columns(sample_rows, ["time", "position"], float_sigfigs=8),
        ["time", "position"],
        "Free-Fall Samples",
        article_images_dir / "freefall_source_data_table",
    )


def generate_plots(tool, plots_dir, freefall_result):
    """Generate log-log error plots and free-fall interpolation figure."""
    for case in TEST_CASES:
        fig, ax = plt.subplots(figsize=(7.0, 4.6))
        x0 = float(case["x"])
        exact = float(case["df"](x0))
        for method in METHODS:
            errors = []
            for h in H_VALUES:
                approx = tool.numerical_differentiation_3point(
                    case["f"], x0, h=float(h), method=method
                )
                errors.append(abs(approx - exact))
            ax.loglog(H_VALUES, errors, label=method)

        ax.set_title(f"Differentiation Error vs h: {case['display_name']}")
        ax.set_xlabel("h")
        ax.set_ylabel("|error|")
        ax.grid(True, which="both", alpha=0.3)
        ax.legend()
        fig.tight_layout()
        stem = plots_dir / CASE_PLOT_STEM_BY_NAME.get(
            case["name"], f"differentiation_{sanitize_filename(case['name'])}_error_vs_h"
        )
        save_figure_png_svg(fig, stem, dpi=300, close_figure=True)

    position_poly, _ = build_freefall_position_interpolant()
    t = np.linspace(
        min(freefall_result["time_data"]),
        max(freefall_result["time_data"]),
        300,
    )
    x = position_poly(t)

    fig, ax = plt.subplots(figsize=(7.0, 4.8))
    ax.plot(t, x, label="Quadratic interpolant", linewidth=2.0)
    ax.scatter(
        freefall_result["time_data"],
        freefall_result["position_data"],
        label="Samples",
        color="black",
        zorder=3,
    )
    t0 = freefall_result["evaluation_time"]
    x0 = float(position_poly(t0))
    ax.scatter([t0], [x0], label=f"Evaluation t0={t0:.4f} s", color="red", zorder=4)
    ax.set_title(
        "Free-Fall Interpolation and |g| Estimate "
        f"({freefall_result['acceleration_magnitude']:.4f} m/s^2)"
    )
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Position (m)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    stem = plots_dir / "freefall_gravity_interpolation"
    save_figure_png_svg(fig, stem, dpi=300, close_figure=True)
