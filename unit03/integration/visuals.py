"""Table images and convergence plots for Unit 03 integration workflow."""

import numpy as np
import matplotlib.pyplot as plt

from unit03.common.table_images import render_table_dual_format
from unit03.integration.config import BENCHMARK_CASES


def _fmt_rows(rows, headers):
    formatted = []
    for row in rows:
        entry = {}
        for key in headers:
            value = row.get(key)
            if isinstance(value, float):
                entry[key] = f"{value:.6e}"
            else:
                entry[key] = str(value)
        formatted.append(entry)
    return formatted


def generate_article_images(method_key, rows, summary_rows, article_images_dir):
    result_headers = ["case_name", "n", "h", "exact", "approx", "abs_error"]
    summary_headers = ["case_name", "observed_order", "final_abs_error", "min_abs_error", "max_abs_error"]

    render_table_dual_format(
        _fmt_rows(rows, result_headers),
        result_headers,
        article_images_dir / f"integration_{method_key}_results_table",
        title=f"Integration {method_key.title()} Results",
    )
    render_table_dual_format(
        _fmt_rows(summary_rows, summary_headers),
        summary_headers,
        article_images_dir / f"integration_{method_key}_summary_table",
        title=f"Integration {method_key.title()} Summary",
    )


def generate_error_plots(method_key, rows, plots_dir):
    for case in BENCHMARK_CASES:
        case_rows = [row for row in rows if row["case_name"] == case["name"]]
        case_rows = sorted(case_rows, key=lambda row: row["h"], reverse=True)
        h_vals = [row["h"] for row in case_rows]
        e_vals = [max(row["abs_error"], np.finfo(float).tiny) for row in case_rows]

        plt.figure(figsize=(6.6, 4.2))
        plt.loglog(h_vals, e_vals, marker="o")
        plt.grid(True, which="both", ls="--", alpha=0.35)
        plt.xlabel("h")
        plt.ylabel("absolute error")
        plt.title(f"{method_key.title()} error vs h: {case['name']}")
        plt.tight_layout()

        stem = plots_dir / f"integration_{method_key}_{case['name']}_error_vs_h"
        plt.savefig(f"{stem}.png", dpi=220)
        plt.savefig(f"{stem}.svg")

        if case["name"] == "x_squared":
            canonical_stem = plots_dir / f"integration_{method_key}_error_vs_h"
            plt.savefig(f"{canonical_stem}.png", dpi=220)
            plt.savefig(f"{canonical_stem}.svg")
        plt.close()
