"""Visualization helpers for differentiation outputs."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .artifacts import format_cell, sanitize_filename
from .calculators import build_summary
from .config import H_VALUES, TEST_CASES


def save_table_image(rows, columns, output_base: Path, title: str):
    """Save a table as both PNG and SVG for article inclusion."""
    cell_text = [[format_cell(row[column], column) for column in columns] for row in rows]

    fig_height = max(2.0, 1.0 + 0.45 * max(1, len(rows)))
    fig_width = max(8.0, 1.2 * len(columns))
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.axis("off")

    table = ax.table(cellText=cell_text, colLabels=columns, loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1.0, 1.25)

    ax.set_title(title, fontsize=11, pad=12)
    fig.tight_layout()
    fig.savefig(output_base.with_suffix(".png"), dpi=300, bbox_inches="tight")
    fig.savefig(output_base.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)


def generate_article_images(rows, article_images_dir: Path, freefall_result: Dict[str, object]):
    """Generate all article table images."""
    summary_rows = build_summary(rows)
    summary_cols = [
        "method",
        "num_cases",
        "all_passed",
        "max_abs_error",
        "mean_abs_error",
        "max_rel_error",
        "mean_rel_error",
    ]
    save_table_image(summary_rows, summary_cols, article_images_dir / "summary_table", "Method Summary")

    result_cols = [
        "case_name",
        "method",
        "x",
        "h",
        "exact",
        "approx",
        "abs_error",
        "rel_error",
        "tolerance",
        "passed",
    ]
    save_table_image(rows, result_cols, article_images_dir / "all_results_table", "All Analytic Results")

    ranked_rows = sorted(rows, key=lambda row: row["abs_error"], reverse=True)
    save_table_image(
        ranked_rows,
        result_cols,
        article_images_dir / "error_ranking_table",
        "Error Ranking (Descending Absolute Error)",
    )

    for case in TEST_CASES:
        case_rows = [row for row in rows if row["case_name"] == case["name"]]
        output_name = sanitize_filename(f"{case['name']}_results_table")
        save_table_image(case_rows, result_cols, article_images_dir / output_name, f"Results for {case['display_name']}")

    freefall_row = {
        "evaluation_time": freefall_result["evaluation_time"],
        "step_size": freefall_result["step_size"],
        "accel_estimate_signed": freefall_result["accel_estimate_signed"],
        "accel_estimate_magnitude": freefall_result["accel_estimate_magnitude"],
        "target_gravity_magnitude": freefall_result["target_gravity_magnitude"],
        "magnitude_abs_error": freefall_result["magnitude_abs_error"],
        "tolerance": freefall_result["tolerance"],
        "passed": freefall_result["passed"],
    }
    save_table_image(
        [freefall_row],
        list(freefall_row.keys()),
        article_images_dir / "freefall_gravity_results_table",
        "Free-Fall Gravity Estimate",
    )

    source_rows = [
        {
            "index": idx,
            "time_s": freefall_result["source_time_data"][idx],
            "position_m": freefall_result["source_position_data"][idx],
        }
        for idx in range(len(freefall_result["source_time_data"]))
    ]
    save_table_image(
        source_rows,
        ["index", "time_s", "position_m"],
        article_images_dir / "freefall_source_data_table",
        "Free-Fall Source Data",
    )


def generate_plots(tool, plots_dir: Path, freefall_result: Dict[str, object]):
    """Generate log-log error plots and the free-fall interpolation visualization."""
    for case in TEST_CASES:
        x = float(case["x"])
        exact = float(case["df"](x))

        fig, ax = plt.subplots(figsize=(7.5, 4.8))
        for method in ("central", "forward", "backward"):
            errors = []
            for h in H_VALUES:
                approx = tool.numerical_differentiation_3point(case["f"], x, h=float(h), method=method)
                errors.append(abs(float(approx) - exact))

            ax.loglog(H_VALUES, np.array(errors), label=method)

        ax.set_xlabel("Step size h")
        ax.set_ylabel("Absolute error")
        ax.set_title(f"3-point error vs h: {case['display_name']}")
        ax.grid(True, which="both", linestyle="--", linewidth=0.6, alpha=0.5)
        ax.legend()
        fig.tight_layout()

        base_name = sanitize_filename(f"{case['name']}_error_vs_h")
        fig.savefig(plots_dir / f"{base_name}.png", dpi=300, bbox_inches="tight")
        fig.savefig(plots_dir / f"{base_name}.svg", bbox_inches="tight")
        plt.close(fig)

    from .calculators import build_freefall_position_interpolant

    position_poly, time_data, position_data = build_freefall_position_interpolant()
    t_dense = np.linspace(float(time_data.min()), float(time_data.max()), 300)
    y_dense = position_poly(t_dense)

    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    ax.plot(t_dense, y_dense, label="Quadratic interpolant", linewidth=2.0)
    ax.scatter(time_data, position_data, label="Sample data", zorder=3)

    t0 = freefall_result["evaluation_time"]
    y0 = float(position_poly(t0))
    ax.scatter([t0], [y0], label="Evaluation point", marker="x", s=90, zorder=4)

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Position (m)")
    ax.set_title(
        "Free-fall interpolation (|g_est| = "
        f"{freefall_result['accel_estimate_magnitude']:.4f} m/s^2)"
    )
    ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.5)
    ax.legend()
    fig.tight_layout()

    fig.savefig(plots_dir / "freefall_gravity_interpolation.png", dpi=300, bbox_inches="tight")
    fig.savefig(plots_dir / "freefall_gravity_interpolation.svg", bbox_inches="tight")
    plt.close(fig)


__all__ = [
    "save_table_image",
    "generate_article_images",
    "generate_plots",
]
