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

N_VALUES = [4, 8, 16, 32, 64, 128, 256]
TRAPEZOIDAL_ORDER_TARGET = 2.0
SIMPSON_ORDER_TARGET = 4.0

BENCHMARK_CASES = (
    {
        "case_name": "poly_x_squared",
        "display_name": "Integral of x^2 on [0, 1]",
        "f": lambda x: x**2,
        "a": 0.0,
        "b": 1.0,
        "exact": 1.0 / 3.0,
        "trap_tol": 3.0e-6,
        "simp_tol": 1.0e-12,
    },
    {
        "case_name": "sin_0_to_pi",
        "display_name": "Integral of sin(x) on [0, pi]",
        "f": np.sin,
        "a": 0.0,
        "b": float(np.pi),
        "exact": 2.0,
        "trap_tol": 3.0e-5,
        "simp_tol": 5.0e-10,
    },
    {
        "case_name": "exp_0_to_1",
        "display_name": "Integral of exp(x) on [0, 1]",
        "f": np.exp,
        "a": 0.0,
        "b": 1.0,
        "exact": float(np.e - 1.0),
        "trap_tol": 3.0e-6,
        "simp_tol": 1.0e-11,
    },
    {
        "case_name": "pi_integral",
        "display_name": "Integral of 4/(1+x^2) on [0, 1]",
        "f": lambda x: 4.0 / (1.0 + x**2),
        "a": 0.0,
        "b": 1.0,
        "exact": float(np.pi),
        "trap_tol": 5.0e-6,
        "simp_tol": 1.0e-11,
    },
)


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


def sanitize_filename(name: str) -> str:
    cleaned = []
    prev_underscore = False

    for char in name.lower():
        if char.isalnum():
            cleaned.append(char)
            prev_underscore = False
        elif not prev_underscore:
            cleaned.append("_")
            prev_underscore = True

    return "".join(cleaned).strip("_") or "case"


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

    for case in BENCHMARK_CASES:
        for n in N_VALUES:
            approx = float(method_callable(case["f"], case["a"], case["b"], n))
            h = (case["b"] - case["a"]) / float(n)
            abs_error = abs(approx - float(case["exact"]))

            rows.append(
                {
                    "case_name": case["case_name"],
                    "display_name": case["display_name"],
                    "method": method_name,
                    "a": float(case["a"]),
                    "b": float(case["b"]),
                    "n": int(n),
                    "h": h,
                    "exact": float(case["exact"]),
                    "approx": approx,
                    "abs_error": abs_error,
                }
            )

    return rows


def observed_order(rows):
    h_values = np.array([row["h"] for row in rows], dtype=float)
    error_values = np.array([row["abs_error"] for row in rows], dtype=float)

    valid = np.isfinite(error_values) & (error_values > 1.0e-15)
    if np.count_nonzero(valid) >= 3:
        h_values = h_values[valid]
        error_values = error_values[valid]
    else:
        # Exact integration can produce all-zero errors for some benchmarks.
        if np.all(error_values <= 1.0e-15):
            return float("inf")
        positive = error_values > 0.0
        if np.count_nonzero(positive) >= 3:
            h_values = h_values[positive]
            error_values = error_values[positive]
        else:
            error_values = np.maximum(error_values, np.finfo(float).tiny)

    slope, _ = np.polyfit(np.log(h_values), np.log(error_values), 1)
    return float(slope)


def build_summary(rows, expected_order: float, tol_key: str):
    summary_rows = []

    for case in BENCHMARK_CASES:
        case_rows = [row for row in rows if row["case_name"] == case["case_name"]]
        finest_row = min(case_rows, key=lambda row: row["h"])
        final_tol = float(case[tol_key])

        summary_rows.append(
            {
                "method": finest_row["method"],
                "case_name": case["case_name"],
                "display_name": case["display_name"],
                "n_values": ",".join(str(row["n"]) for row in case_rows),
                "num_runs": len(case_rows),
                "expected_order": expected_order,
                "observed_order": observed_order(case_rows),
                "finest_n": int(finest_row["n"]),
                "finest_h": float(finest_row["h"]),
                "finest_approx": float(finest_row["approx"]),
                "exact": float(case["exact"]),
                "finest_abs_error": float(finest_row["abs_error"]),
                "final_tolerance": final_tol,
                "passed_final_tolerance": float(finest_row["abs_error"]) <= final_tol,
            }
        )

    return summary_rows


def write_method_outputs(method_slug: str, rows, summary_rows):
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
        "display_name",
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
        file.write(f"# {method_slug.title()} Integration Results\n\n")
        file.write(markdown_table(rows, result_columns) + "\n")

    summary_csv_path = ARTICLE_RESULTS_DIR / f"integration_{method_slug}_summary.csv"
    with summary_csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=summary_columns)
        writer.writeheader()
        writer.writerows(summary_rows)

    metadata = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "method": method_slug,
        "benchmark_cases": [
            {
                "case_name": case["case_name"],
                "display_name": case["display_name"],
                "a": float(case["a"]),
                "b": float(case["b"]),
                "exact": float(case["exact"]),
            }
            for case in BENCHMARK_CASES
        ],
        "n_values": N_VALUES,
        "case_summaries": summary_rows,
    }
    metadata_path = ARTICLE_RESULTS_DIR / f"integration_{method_slug}_metadata.json"
    with metadata_path.open("w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2)


def generate_error_plots(method_slug: str, rows, expected_order: float):
    for case in BENCHMARK_CASES:
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
        fig.savefig(PLOTS_DIR / f"{base}.png", dpi=300, bbox_inches="tight")
        fig.savefig(PLOTS_DIR / f"{base}.svg", bbox_inches="tight")
        plt.close(fig)


def generate_article_images(method_slug: str, rows, summary_rows):
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
        ARTICLE_IMAGES_DIR / f"integration_{method_slug}_results_table",
        f"{method_slug.title()} integration results",
    )
    save_table_image(
        summary_rows,
        summary_columns,
        ARTICLE_IMAGES_DIR / f"integration_{method_slug}_summary_table",
        f"{method_slug.title()} integration summary",
    )


def write_unittest_report(trapezoidal_summary_rows, simpson_summary_rows):
    lines = [
        "Unit 03 Integration Report",
        "=" * 26,
        "",
        "Benchmarks:",
    ]

    for case in BENCHMARK_CASES:
        lines.append(
            f"- {case['case_name']}: {case['display_name']} (exact = {float(case['exact']):.12f})"
        )

    lines.extend(
        [
            "",
            "method | case_name | expected_order | observed_order | finest_n | finest_abs_error | final_tolerance | passed_final_tolerance",
        ]
    )

    for summary in trapezoidal_summary_rows + simpson_summary_rows:
        lines.append(
            f"{summary['method']} | {summary['case_name']} | {summary['expected_order']:.1f} | "
            f"{summary['observed_order']:.6f} | {summary['finest_n']} | {summary['finest_abs_error']:.6e} | "
            f"{summary['final_tolerance']:.6e} | {summary['passed_final_tolerance']}"
        )

    report_path = ARTICLE_RESULTS_DIR / "integration_unittest_report.txt"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_all_outputs(tool: IntegrationTools):
    ensure_output_dirs()

    trapezoidal_rows = collect_method_results(tool, "trapezoidal", tool.composite_trapezoidal)
    simpson_rows = collect_method_results(tool, "simpson", tool.composite_simpson)

    trapezoidal_summary_rows = build_summary(
        trapezoidal_rows,
        expected_order=TRAPEZOIDAL_ORDER_TARGET,
        tol_key="trap_tol",
    )
    simpson_summary_rows = build_summary(
        simpson_rows,
        expected_order=SIMPSON_ORDER_TARGET,
        tol_key="simp_tol",
    )

    write_method_outputs("trapezoidal", trapezoidal_rows, trapezoidal_summary_rows)
    write_method_outputs("simpson", simpson_rows, simpson_summary_rows)
    generate_error_plots("trapezoidal", trapezoidal_rows, TRAPEZOIDAL_ORDER_TARGET)
    generate_error_plots("simpson", simpson_rows, SIMPSON_ORDER_TARGET)
    generate_article_images("trapezoidal", trapezoidal_rows, trapezoidal_summary_rows)
    generate_article_images("simpson", simpson_rows, simpson_summary_rows)
    write_unittest_report(trapezoidal_summary_rows, simpson_summary_rows)

    return {
        "trapezoidal_rows": trapezoidal_rows,
        "simpson_rows": simpson_rows,
        "trapezoidal_summary_rows": trapezoidal_summary_rows,
        "simpson_summary_rows": simpson_summary_rows,
    }


class TestIntegrationMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool = IntegrationTools()
        cls.generated = generate_all_outputs(cls.tool)

    def test_trapezoidal_final_accuracy(self):
        failures = [
            row
            for row in self.generated["trapezoidal_summary_rows"]
            if not row["passed_final_tolerance"]
        ]
        self.assertFalse(failures, msg=f"Trapezoidal tolerance failures: {failures}")

    def test_simpson_final_accuracy(self):
        failures = [
            row
            for row in self.generated["simpson_summary_rows"]
            if not row["passed_final_tolerance"]
        ]
        self.assertFalse(failures, msg=f"Simpson tolerance failures: {failures}")

    def test_observed_orders(self):
        for row in self.generated["trapezoidal_summary_rows"]:
            self.assertGreater(row["observed_order"], 1.8)
        for row in self.generated["simpson_summary_rows"]:
            self.assertGreater(row["observed_order"], 3.8)

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
        ]

        for method in ("trapezoidal", "simpson"):
            for case in BENCHMARK_CASES:
                base = f"integration_{method}_{sanitize_filename(case['case_name'])}_error_vs_h"
                expected_paths.append(PLOTS_DIR / f"{base}.png")
                expected_paths.append(PLOTS_DIR / f"{base}.svg")

        missing = [str(path) for path in expected_paths if not path.exists()]
        self.assertFalse(missing, msg="Missing expected output files:\n" + "\n".join(missing))

    def test_trapezoidal_validation(self):
        case = BENCHMARK_CASES[0]
        with self.assertRaises(TypeError):
            self.tool.composite_trapezoidal(123, case["a"], case["b"], 4)
        with self.assertRaises(ValueError):
            self.tool.composite_trapezoidal(case["f"], case["a"], case["b"], 0)
        with self.assertRaises(ValueError):
            self.tool.composite_trapezoidal(case["f"], case["a"], case["a"], 4)

    def test_simpson_validation(self):
        case = BENCHMARK_CASES[0]
        with self.assertRaises(TypeError):
            self.tool.composite_simpson(None, case["a"], case["b"], 4)
        with self.assertRaises(ValueError):
            self.tool.composite_simpson(case["f"], case["a"], case["b"], 0)
        with self.assertRaises(ValueError):
            self.tool.composite_simpson(case["f"], case["a"], case["b"], 3)
        with self.assertRaises(ValueError):
            self.tool.composite_simpson(case["f"], case["a"], case["a"], 4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
