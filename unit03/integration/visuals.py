"""Visualization utilities for Unit 03 integration workflows."""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from unit03.common.artifact_io import format_rows_for_columns
from unit03.common.table_images import render_table_image, save_figure_png_svg


def generate_article_images(method, rows, summary_rows, article_images_dir):
    """Generate per-method result and summary table images."""
    result_cols = ["case", "n", "h", "exact", "approx", "abs_error", "rel_error"]
    summary_cols = [
        "case",
        "observed_order",
        "best_n",
        "best_abs_error",
        "final_n",
        "final_abs_error",
    ]

    render_table_image(
        format_rows_for_columns(rows, result_cols, float_sigfigs=8),
        result_cols,
        f"Integration {method.title()} Results",
        article_images_dir / f"integration_{method}_results_table",
    )
    render_table_image(
        format_rows_for_columns(summary_rows, summary_cols, float_sigfigs=8),
        summary_cols,
        f"Integration {method.title()} Summary",
        article_images_dir / f"integration_{method}_summary_table",
    )


def generate_error_plots(method, rows, plots_dir):
    """Generate log-log error-vs-h plots for each benchmark case."""
    case_names = sorted({row["case"] for row in rows})
    for case_name in case_names:
        case_rows = sorted(
            [row for row in rows if row["case"] == case_name],
            key=lambda row: row["n"],
        )
        h_values = [row["h"] for row in case_rows]
        errors = [row["abs_error"] for row in case_rows]
        plot_errors = [max(err, 1e-300) for err in errors]
        display_name = case_rows[0]["case_display"]

        fig, ax = plt.subplots(figsize=(7.0, 4.6))
        ax.loglog(h_values, plot_errors, marker="o", linewidth=1.8)
        ax.set_title(f"{method.title()} Error vs h: {display_name}")
        ax.set_xlabel("h")
        ax.set_ylabel("|error|")
        ax.grid(True, which="both", alpha=0.3)
        fig.tight_layout()
        if case_name == "x_squared":
            stem = plots_dir / f"integration_{method}_error_vs_h"
        else:
            stem = plots_dir / f"integration_{method}_{case_name}_error_vs_h"
        save_figure_png_svg(fig, stem, dpi=300, close_figure=True)
