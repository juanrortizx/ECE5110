"""Visualization helpers for integration workflows."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .artifacts import format_cell, sanitize_filename
from .calculators import observed_order


def save_table_image(rows, columns, output_base: Path, title: str):
    cell_text = [[format_cell(row[column]) for column in columns] for row in rows]

    fig_height = max(2.0, 1.0 + 0.45 * max(1, len(rows)))
    fig_width = max(8.0, 1.15 * len(columns))
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.axis("off")

    table = ax.table(cellText=cell_text, colLabels=columns, loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1.0, 1.2)

    ax.set_title(title, fontsize=11, pad=12)
    fig.tight_layout()
    fig.savefig(output_base.with_suffix(".png"), dpi=300, bbox_inches="tight")
    fig.savefig(output_base.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)


def generate_article_images(method_slug: str, rows, summary_rows, article_images_dir: Path):
    result_columns = ["case_name", "n", "h", "exact", "approx", "abs_error"]
    summary_columns = [
        "method",
        "case_name",
        "expected_order",
        "observed_order",
        "finest_n",
        "finest_abs_error",
        "final_tolerance",
        "passed_final_tolerance",
    ]

    save_table_image(
        rows,
        result_columns,
        article_images_dir / f"integration_{method_slug}_results_table",
        f"{method_slug.title()} integration results",
    )
    save_table_image(
        summary_rows,
        summary_columns,
        article_images_dir / f"integration_{method_slug}_summary_table",
        f"{method_slug.title()} integration summary",
    )


def generate_error_plots(method_slug: str, rows, expected_order: float, plots_dir: Path, benchmark_cases):
    for case in benchmark_cases:
        case_rows = [row for row in rows if row["case_name"] == case["case_name"]]
        h_values = np.array([row["h"] for row in case_rows], dtype=float)
        errors = np.array([row["abs_error"] for row in case_rows], dtype=float)
        errors_plot = np.maximum(errors, np.finfo(float).tiny)

        fig, ax = plt.subplots(figsize=(7.5, 4.8))
        ax.loglog(h_values, errors_plot, marker="o", linewidth=2.0)
        ax.set_xlabel("Step size h")
        ax.set_ylabel("Absolute error")
        ax.set_title(f"{method_slug.title()} error vs h: {case['display_name']}")
        ax.grid(True, which="both", linestyle="--", linewidth=0.6, alpha=0.5)
        ax.text(
            0.05,
            0.05,
            f"expected order = {expected_order:.0f}\nobserved order = {observed_order(case_rows):.4f}",
            transform=ax.transAxes,
            fontsize=9,
            bbox={"facecolor": "white", "alpha": 0.85, "edgecolor": "0.6"},
        )
        fig.tight_layout()

        base = f"integration_{method_slug}_{sanitize_filename(case['case_name'])}_error_vs_h"
        fig.savefig(plots_dir / f"{base}.png", dpi=300, bbox_inches="tight")
        fig.savefig(plots_dir / f"{base}.svg", bbox_inches="tight")
        plt.close(fig)


__all__ = ["save_table_image", "generate_article_images", "generate_error_plots"]
