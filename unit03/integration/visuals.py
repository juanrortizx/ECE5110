"""Visualization utilities for Unit 03 integration workflows."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .config import BENCHMARK_CASES


def save_table_image(headers, row_dicts, output_stem, title=""):
    """Render a table image and save to PNG/SVG."""
    cell_text = [[str(row.get(h, "")) for h in headers] for row in row_dicts]
    nrows = max(2, len(cell_text) + 1)

    fig, ax = plt.subplots(figsize=(max(8, len(headers) * 1.5), 0.5 * nrows + 1.0))
    ax.axis("off")
    table = ax.table(cellText=cell_text, colLabels=headers, loc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1.0, 1.2)
    if title:
        ax.set_title(title, fontsize=10, pad=10)
    fig.tight_layout()

    fig.savefig(f"{output_stem}.png", dpi=300, bbox_inches="tight")
    fig.savefig(f"{output_stem}.svg", bbox_inches="tight")
    plt.close(fig)


def generate_article_images(method_key, rows, summary_rows, article_images_dir):
    """Generate method-specific results and summary table images."""
    save_table_image(
        list(rows[0].keys()) if rows else [],
        rows,
        str(article_images_dir / f"integration_{method_key}_results_table"),
        title=f"Integration {method_key.title()} Results",
    )
    save_table_image(
        list(summary_rows[0].keys()) if summary_rows else [],
        summary_rows,
        str(article_images_dir / f"integration_{method_key}_summary_table"),
        title=f"Integration {method_key.title()} Summary",
    )


def generate_error_plots(method_key, rows, plots_dir):
    """Generate log-log absolute error plots for each benchmark case."""
    for case in BENCHMARK_CASES:
        case_rows = [row for row in rows if row["case_name"] == case["name"]]
        hs = np.array([row["h"] for row in case_rows], dtype=float)
        errors = np.array([row["abs_error"] for row in case_rows], dtype=float)
        errors = np.maximum(errors, np.finfo(float).tiny)

        fig, ax = plt.subplots(figsize=(7, 5))
        ax.loglog(hs, errors, marker="o", linewidth=1.5)
        ax.set_xlabel("h")
        ax.set_ylabel("Absolute error")
        ax.set_title(f"{method_key.title()} error vs h: {case['name']}")
        ax.grid(True, which="both", linestyle="--", alpha=0.3)
        fig.tight_layout()

        stem = plots_dir / f"integration_{method_key}_{case['name']}_error_vs_h"
        fig.savefig(f"{stem}.png", dpi=300, bbox_inches="tight")
        fig.savefig(f"{stem}.svg", bbox_inches="tight")
        plt.close(fig)
