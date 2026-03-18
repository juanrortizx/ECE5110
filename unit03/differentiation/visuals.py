"""Visualization utilities for Unit 03 differentiation workflow."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .artifacts import sanitize_filename
from .config import FREEFALL_TIME_DATA, H_VALUES, METHODS, TEST_CASES


def save_table_image(headers, row_dicts, output_stem, title=""):
    """Render a small table figure and export both PNG and SVG."""
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


def generate_article_images(rows, article_images_dir, freefall_result):
    """Generate summary, full-results, per-case, and free-fall table images."""
    summary_rows = []
    for method in METHODS:
        method_rows = [r for r in rows if r["method"] == method]
        summary_rows.append(
            {
                "method": method,
                "pass_count": sum(1 for r in method_rows if r["pass"]),
                "num_cases": len(method_rows),
                "max_abs_error": max(r["abs_error"] for r in method_rows),
            }
        )

    save_table_image(
        ["method", "pass_count", "num_cases", "max_abs_error"],
        summary_rows,
        str(article_images_dir / "summary_table"),
        title="Differentiation Summary",
    )

    all_headers = [
        "case_name",
        "method",
        "exact",
        "approx",
        "abs_error",
        "rel_error",
        "tolerance",
        "pass",
    ]
    save_table_image(
        all_headers,
        rows,
        str(article_images_dir / "all_results_table"),
        title="Differentiation Results",
    )

    ranking_rows = sorted(rows, key=lambda row: row["abs_error"], reverse=True)
    save_table_image(
        ["case_name", "method", "abs_error", "rel_error", "pass"],
        ranking_rows,
        str(article_images_dir / "error_ranking_table"),
        title="Error Ranking",
    )

    for case in TEST_CASES:
        case_rows = [r for r in rows if r["case_name"] == case["name"]]
        save_table_image(
            all_headers,
            case_rows,
            str(article_images_dir / f"{sanitize_filename(case['name'])}_results_table"),
            title=case["display_name"],
        )

    freefall_table = [
        {
            "evaluation_time": freefall_result["evaluation_time"],
            "acceleration_signed": freefall_result["acceleration_signed"],
            "acceleration_magnitude": freefall_result["acceleration_magnitude"],
            "target_gravity_magnitude": freefall_result["target_gravity_magnitude"],
            "magnitude_abs_error": freefall_result["magnitude_abs_error"],
            "tolerance": freefall_result["tolerance"],
            "pass": freefall_result["pass"],
        }
    ]
    save_table_image(
        list(freefall_table[0].keys()),
        freefall_table,
        str(article_images_dir / "freefall_gravity_results_table"),
        title="Free-Fall Gravity Validation",
    )

    source_rows = [
        {"time_s": t, "position_m": y}
        for t, y in zip(
            freefall_result["source_time_data"],
            freefall_result["source_position_data"],
        )
    ]
    save_table_image(
        ["time_s", "position_m"],
        source_rows,
        str(article_images_dir / "freefall_source_data_table"),
        title="Free-Fall Source Data",
    )


def generate_plots(tool, plots_dir, freefall_result):
    """Generate log-log error plots and free-fall interpolation visual."""
    for case in TEST_CASES:
        x0 = case["x"]
        exact = float(case["df"](x0))

        fig, ax = plt.subplots(figsize=(7, 5))
        for method in METHODS:
            errors = []
            for h in H_VALUES:
                approx = tool.numerical_differentiation_3point(case["f"], x0, h=h, method=method)
                errors.append(abs(approx - exact))
            ax.loglog(H_VALUES, errors, label=method)

        ax.set_xlabel("h")
        ax.set_ylabel("Absolute error")
        ax.set_title(f"{case['display_name']} error vs h")
        ax.grid(True, which="both", linestyle="--", alpha=0.3)
        ax.legend()
        fig.tight_layout()

        stem = plots_dir / f"{sanitize_filename(case['name'])}_error_vs_h"
        fig.savefig(f"{stem}.png", dpi=300, bbox_inches="tight")
        fig.savefig(f"{stem}.svg", bbox_inches="tight")
        plt.close(fig)

    coeffs = np.array(freefall_result["poly_coefficients"], dtype=float)
    poly = np.poly1d(coeffs)
    time_data = np.array(freefall_result["source_time_data"], dtype=float)
    pos_data = np.array(freefall_result["source_position_data"], dtype=float)

    t_dense = np.linspace(time_data.min(), time_data.max(), 300)
    p_dense = poly(t_dense)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(t_dense, p_dense, label="quadratic interpolant")
    ax.scatter(time_data, pos_data, c="black", s=20, label="measured data")
    ax.scatter(
        [freefall_result["evaluation_time"]],
        [poly(freefall_result["evaluation_time"])],
        c="red",
        s=40,
        label=f"evaluation point (|g|={freefall_result['acceleration_magnitude']:.3f})",
    )
    ax.set_xlabel("time (s)")
    ax.set_ylabel("position (m)")
    ax.set_title("Free-fall interpolation and gravity estimate")
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.legend()
    fig.tight_layout()

    stem = plots_dir / "freefall_gravity_interpolation"
    fig.savefig(f"{stem}.png", dpi=300, bbox_inches="tight")
    fig.savefig(f"{stem}.svg", bbox_inches="tight")
    plt.close(fig)
