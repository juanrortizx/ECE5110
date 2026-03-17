import csv
import json
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lib.integration_tools import IntegrationTools

UNIT_RESULTS_DIR = PROJECT_ROOT / "unit03" / "results"
ARTICLE_RESULTS_DIR = UNIT_RESULTS_DIR / "article_results"
PLOTS_DIR = UNIT_RESULTS_DIR / "plots"
ARTICLE_IMAGES_DIR = UNIT_RESULTS_DIR / "article_images"

CASE_NAME = "pi_integral"
DISPLAY_NAME = "Integral of 4/(1+x^2) on [0, 1]"
LOWER_BOUND = 0.0
UPPER_BOUND = 1.0
EXACT_VALUE = float(np.pi)
N_VALUES = [4, 8, 16, 32, 64, 128, 256]
TRAPEZOIDAL_ORDER_TARGET = 2.0
SIMPSON_ORDER_TARGET = 4.0
TRAPEZOIDAL_FINAL_TOL = 2.0e-5
SIMPSON_FINAL_TOL = 1.0e-9


def integrand(x):
    return 4.0 / (1.0 + x**2)


def ensure_output_dirs():
    ARTICLE_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    ARTICLE_IMAGES_DIR.mkdir(parents=True, exist_ok=True)


def format_cell(value):
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, (int, np.integer)):
        return str(int(value))
    if isinstance(value, (float, np.floating)):
        return f"{float(value):.6e}"
    return str(value)


def markdown_table(rows, columns):
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []

    for row in rows:
        body.append("| " + " | ".join(format_cell(row[column]) for column in columns) + " |")

    return "\n".join([header, separator] + body)


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


def collect_method_results(tool: IntegrationTools, method_name: str, method_callable):
    rows = []

    for n in N_VALUES:
        approx = float(method_callable(integrand, LOWER_BOUND, UPPER_BOUND, n))
        h = (UPPER_BOUND - LOWER_BOUND) / float(n)
        abs_error = abs(approx - EXACT_VALUE)

        rows.append(
            {
                "case_name": CASE_NAME,
                "display_name": DISPLAY_NAME,
                "method": method_name,
                "a": LOWER_BOUND,
                "b": UPPER_BOUND,
                "n": int(n),
                "h": h,
                "exact": EXACT_VALUE,
                "approx": approx,
                "abs_error": abs_error,
            }
        )

    return rows


def observed_order(rows):
    h_values = np.array([row["h"] for row in rows], dtype=float)
    error_values = np.array([row["abs_error"] for row in rows], dtype=float)

    valid = error_values > 1.0e-10
    if np.count_nonzero(valid) >= 3:
        h_values = h_values[valid]
        error_values = error_values[valid]
    else:
        top_indices = np.argsort(error_values)[-max(3, min(len(error_values), 3)):]
        h_values = h_values[top_indices]
        error_values = error_values[top_indices]

    slope, _ = np.polyfit(np.log(h_values), np.log(error_values), 1)
    return float(slope)


def build_summary(rows, expected_order: float, final_tol: float):
    finest_row = min(rows, key=lambda row: row["h"])
    order = observed_order(rows)

    return {
        "method": finest_row["method"],
        "case_name": CASE_NAME,
        "n_values": ",".join(str(row["n"]) for row in rows),
        "num_runs": len(rows),
        "expected_order": expected_order,
        "observed_order": order,
        "finest_n": int(finest_row["n"]),
        "finest_h": float(finest_row["h"]),
        "finest_approx": float(finest_row["approx"]),
        "exact": EXACT_VALUE,
        "finest_abs_error": float(finest_row["abs_error"]),
        "final_tolerance": final_tol,
        "passed_final_tolerance": float(finest_row["abs_error"]) <= final_tol,
    }


def write_method_outputs(method_slug: str, rows, summary):
    result_columns = [
        "case_name",
        "display_name",
        "method",
        "a",
        "b",
        "n",
        "h",
        "exact",
        "approx",
        "abs_error",
    ]
    summary_columns = [
        "method",
        "case_name",
        "n_values",
        "num_runs",
        "expected_order",
        "observed_order",
        "finest_n",
        "finest_h",
        "finest_approx",
        "exact",
        "finest_abs_error",
        "final_tolerance",
        "passed_final_tolerance",
    ]

    csv_path = ARTICLE_RESULTS_DIR / f"integration_{method_slug}_results.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=result_columns)
        writer.writeheader()
        writer.writerows(rows)

    json_path = ARTICLE_RESULTS_DIR / f"integration_{method_slug}_results.json"
    with json_path.open("w", encoding="utf-8") as file:
        json.dump(rows, file, indent=2)

    md_path = ARTICLE_RESULTS_DIR / f"integration_{method_slug}_results.md"
    with md_path.open("w", encoding="utf-8") as file:
        file.write(f"# {summary['method'].title()} Integration Results\n\n")
        file.write(markdown_table(rows, result_columns) + "\n")

    summary_csv_path = ARTICLE_RESULTS_DIR / f"integration_{method_slug}_summary.csv"
    with summary_csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=summary_columns)
        writer.writeheader()
        writer.writerow(summary)

    metadata = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "case_name": CASE_NAME,
        "display_name": DISPLAY_NAME,
        "method": summary["method"],
        "exact_integral": EXACT_VALUE,
        "integration_bounds": [LOWER_BOUND, UPPER_BOUND],
        "n_values": N_VALUES,
        "expected_order": summary["expected_order"],
        "observed_order": summary["observed_order"],
        "final_tolerance": summary["final_tolerance"],
        "passed_final_tolerance": summary["passed_final_tolerance"],
    }
    metadata_path = ARTICLE_RESULTS_DIR / f"integration_{method_slug}_metadata.json"
    with metadata_path.open("w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2)


def generate_error_plot(method_slug: str, rows, expected_order: float):
    h_values = np.array([row["h"] for row in rows], dtype=float)
    errors = np.array([row["abs_error"] for row in rows], dtype=float)

    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    ax.loglog(h_values, errors, marker="o", linewidth=2.0)
    ax.set_xlabel("Step size h")
    ax.set_ylabel("Absolute error")
    ax.set_title(
        f"{rows[0]['method'].title()} error vs h for integral of 4/(1+x^2)"
    )
    ax.grid(True, which="both", linestyle="--", linewidth=0.6, alpha=0.5)
    ax.text(
        0.05,
        0.05,
        f"expected order = {expected_order:.0f}\nobserved order = {observed_order(rows):.4f}",
        transform=ax.transAxes,
        fontsize=9,
        bbox={"facecolor": "white", "alpha": 0.85, "edgecolor": "0.6"},
    )
    fig.tight_layout()
    fig.savefig(PLOTS_DIR / f"integration_{method_slug}_error_vs_h.png", dpi=300, bbox_inches="tight")
    fig.savefig(PLOTS_DIR / f"integration_{method_slug}_error_vs_h.svg", bbox_inches="tight")
    plt.close(fig)


def generate_article_images(method_slug: str, rows, summary):
    result_columns = ["n", "h", "exact", "approx", "abs_error"]
    summary_columns = [
        "method",
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
        ARTICLE_IMAGES_DIR / f"integration_{method_slug}_results_table",
        f"{summary['method'].title()} integration results",
    )
    save_table_image(
        [summary],
        summary_columns,
        ARTICLE_IMAGES_DIR / f"integration_{method_slug}_summary_table",
        f"{summary['method'].title()} integration summary",
    )


def write_unittest_report(trapezoidal_summary, simpson_summary):
    lines = [
        "Unit 03 Integration Report",
        "=" * 26,
        "",
        f"case_name: {CASE_NAME}",
        f"display_name: {DISPLAY_NAME}",
        f"exact_integral: {EXACT_VALUE:.12f}",
        "",
        "method | expected_order | observed_order | finest_n | finest_abs_error | final_tolerance | passed_final_tolerance",
    ]

    for summary in (trapezoidal_summary, simpson_summary):
        lines.append(
            f"{summary['method']} | {summary['expected_order']:.1f} | {summary['observed_order']:.6f} | "
            f"{summary['finest_n']} | {summary['finest_abs_error']:.6e} | "
            f"{summary['final_tolerance']:.6e} | {summary['passed_final_tolerance']}"
        )

    report_path = ARTICLE_RESULTS_DIR / "integration_unittest_report.txt"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_all_outputs(tool: IntegrationTools):
    ensure_output_dirs()

    trapezoidal_rows = collect_method_results(tool, "trapezoidal", tool.composite_trapezoidal)
    simpson_rows = collect_method_results(tool, "simpson", tool.composite_simpson)

    trapezoidal_summary = build_summary(
        trapezoidal_rows,
        expected_order=TRAPEZOIDAL_ORDER_TARGET,
        final_tol=TRAPEZOIDAL_FINAL_TOL,
    )
    simpson_summary = build_summary(
        simpson_rows,
        expected_order=SIMPSON_ORDER_TARGET,
        final_tol=SIMPSON_FINAL_TOL,
    )

    write_method_outputs("trapezoidal", trapezoidal_rows, trapezoidal_summary)
    write_method_outputs("simpson", simpson_rows, simpson_summary)
    generate_error_plot("trapezoidal", trapezoidal_rows, TRAPEZOIDAL_ORDER_TARGET)
    generate_error_plot("simpson", simpson_rows, SIMPSON_ORDER_TARGET)
    generate_article_images("trapezoidal", trapezoidal_rows, trapezoidal_summary)
    generate_article_images("simpson", simpson_rows, simpson_summary)
    write_unittest_report(trapezoidal_summary, simpson_summary)

    return {
        "trapezoidal_rows": trapezoidal_rows,
        "simpson_rows": simpson_rows,
        "trapezoidal_summary": trapezoidal_summary,
        "simpson_summary": simpson_summary,
    }


class TestIntegrationMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool = IntegrationTools()
        cls.generated = generate_all_outputs(cls.tool)

    def test_trapezoidal_final_accuracy(self):
        finest = self.generated["trapezoidal_summary"]
        self.assertLessEqual(finest["finest_abs_error"], TRAPEZOIDAL_FINAL_TOL)

    def test_simpson_final_accuracy(self):
        finest = self.generated["simpson_summary"]
        self.assertLessEqual(finest["finest_abs_error"], SIMPSON_FINAL_TOL)

    def test_observed_orders(self):
        self.assertGreater(self.generated["trapezoidal_summary"]["observed_order"], 1.8)
        self.assertGreater(self.generated["simpson_summary"]["observed_order"], 3.8)

    def test_required_outputs_exist(self):
        expected_paths = [
            ARTICLE_RESULTS_DIR / "integration_trapezoidal_results.csv",
            ARTICLE_RESULTS_DIR / "integration_trapezoidal_results.json",
            ARTICLE_RESULTS_DIR / "integration_trapezoidal_results.md",
            ARTICLE_RESULTS_DIR / "integration_trapezoidal_summary.csv",
            ARTICLE_RESULTS_DIR / "integration_trapezoidal_metadata.json",
            ARTICLE_RESULTS_DIR / "integration_simpson_results.csv",
            ARTICLE_RESULTS_DIR / "integration_simpson_results.json",
            ARTICLE_RESULTS_DIR / "integration_simpson_results.md",
            ARTICLE_RESULTS_DIR / "integration_simpson_summary.csv",
            ARTICLE_RESULTS_DIR / "integration_simpson_metadata.json",
            ARTICLE_RESULTS_DIR / "integration_unittest_report.txt",
            PLOTS_DIR / "integration_trapezoidal_error_vs_h.png",
            PLOTS_DIR / "integration_simpson_error_vs_h.png",
        ]

        missing = [str(path) for path in expected_paths if not path.exists()]
        self.assertFalse(missing, msg="Missing expected output files:\n" + "\n".join(missing))

    def test_trapezoidal_validation(self):
        with self.assertRaises(TypeError):
            self.tool.composite_trapezoidal(123, LOWER_BOUND, UPPER_BOUND, 4)
        with self.assertRaises(ValueError):
            self.tool.composite_trapezoidal(integrand, LOWER_BOUND, UPPER_BOUND, 0)
        with self.assertRaises(ValueError):
            self.tool.composite_trapezoidal(integrand, LOWER_BOUND, LOWER_BOUND, 4)

    def test_simpson_validation(self):
        with self.assertRaises(TypeError):
            self.tool.composite_simpson(None, LOWER_BOUND, UPPER_BOUND, 4)
        with self.assertRaises(ValueError):
            self.tool.composite_simpson(integrand, LOWER_BOUND, UPPER_BOUND, 0)
        with self.assertRaises(ValueError):
            self.tool.composite_simpson(integrand, LOWER_BOUND, UPPER_BOUND, 3)
        with self.assertRaises(ValueError):
            self.tool.composite_simpson(integrand, LOWER_BOUND, LOWER_BOUND, 4)


if __name__ == "__main__":
    unittest.main(verbosity=2)