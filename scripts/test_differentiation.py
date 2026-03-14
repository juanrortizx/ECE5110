"""
scripts/test_differentiation.py
--------------------------------
Unit tests and reproducible results generator for 3-point numerical
differentiation (ECE 5110).

Run directly:
    python scripts/test_differentiation.py

Or via unittest:
    python -m unittest scripts.test_differentiation
"""

import csv
import json
import re
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")          # headless backend – no display required
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

from lib.differentiation_tools import DifferentiationTools  # noqa: E402

# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------
TEST_CASES = [
    {
        "name": "sine_at_pi_over_4",
        "display": "sin(x) at x = π/4",
        "f": np.sin,
        "df": np.cos,
        "x": np.pi / 4,
        "h": 1e-5,
        "tol": {"central": 1e-9, "forward": 1e-9, "backward": 1e-9},
    },
    {
        "name": "exp_at_0p3",
        "display": "exp(x) at x = 0.3",
        "f": np.exp,
        "df": np.exp,
        "x": 0.3,
        "h": 1e-5,
        "tol": {"central": 1e-9, "forward": 1e-9, "backward": 1e-9},
    },
    {
        "name": "poly_at_1p2",
        "display": "x³ − 2x² + x − 5 at x = 1.2",
        "f": lambda x: x**3 - 2 * x**2 + x - 5,
        "df": lambda x: 3 * x**2 - 4 * x + 1,
        "x": 1.2,
        "h": 1e-5,
        "tol": {"central": 1e-8, "forward": 1e-8, "backward": 1e-8},
    },
]

METHODS = ("central", "forward", "backward")
H_VALUES = np.logspace(-1, -8, 80)

# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def create_run_output_dirs(base_dir: Path):
    """Scan base_dir for unitXX_test_results folders and create the next one.

    Returns
    -------
    tuple
        (run_dir, article_results_dir, plots_dir, article_images_dir, run_index)
    """
    pattern = re.compile(r"^unit(\d+)_test_results$")
    existing = [
        int(m.group(1))
        for p in base_dir.iterdir()
        if p.is_dir() and (m := pattern.match(p.name))
    ]
    run_index = max(existing, default=0) + 1
    run_dir = base_dir / f"unit{run_index:02d}_test_results"

    article_results_dir = run_dir / "article_results"
    plots_dir = run_dir / "plots"
    article_images_dir = run_dir / "article_images"

    for d in (article_results_dir, plots_dir, article_images_dir):
        d.mkdir(parents=True, exist_ok=True)

    return run_dir, article_results_dir, plots_dir, article_images_dir, run_index


def sanitize_filename(name: str) -> str:
    """Return a safe lowercase filename by replacing non-alphanumeric chars with '_'."""
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


# ---------------------------------------------------------------------------
# Result collection
# ---------------------------------------------------------------------------

def collect_results(tool: DifferentiationTools):
    """Evaluate all test cases × methods and return a list of row dicts."""
    rows = []
    for case in TEST_CASES:
        exact = float(case["df"](case["x"]))
        for method in METHODS:
            approx = tool.numerical_differentiation_3point(
                case["f"], case["x"], h=case["h"], method=method
            )
            abs_err = abs(approx - exact)
            rel_err = abs_err / abs(exact) if exact != 0 else float("nan")
            tol = case["tol"][method]
            passed = abs_err <= tol
            rows.append(
                {
                    "case_name": case["name"],
                    "case_display": case["display"],
                    "method": method,
                    "x": case["x"],
                    "h": case["h"],
                    "exact": exact,
                    "approx": approx,
                    "abs_error": abs_err,
                    "rel_error": rel_err,
                    "tolerance": tol,
                    "passed": passed,
                }
            )
    return rows


def build_summary(rows):
    """Summarise rows by method.

    Returns a list of summary dicts, one per method.
    """
    summary = []
    for method in METHODS:
        method_rows = [r for r in rows if r["method"] == method]
        abs_errors = [r["abs_error"] for r in method_rows]
        rel_errors = [r["rel_error"] for r in method_rows if not np.isnan(r["rel_error"])]
        summary.append(
            {
                "method": method,
                "n_cases": len(method_rows),
                "all_passed": all(r["passed"] for r in method_rows),
                "max_abs_error": max(abs_errors),
                "mean_abs_error": float(np.mean(abs_errors)),
                "max_rel_error": max(rel_errors) if rel_errors else float("nan"),
                "mean_rel_error": float(np.mean(rel_errors)) if rel_errors else float("nan"),
            }
        )
    return summary


# ---------------------------------------------------------------------------
# File saving
# ---------------------------------------------------------------------------

def save_results(rows, article_results_dir: Path, run_index: int):
    """Save CSV, JSON, Markdown, summary CSV, and run metadata."""

    # --- CSV (full results) ---
    csv_cols = [
        "case_name", "case_display", "method", "x", "h",
        "exact", "approx", "abs_error", "rel_error", "tolerance", "passed",
    ]
    csv_path = article_results_dir / "differentiation_test_results.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=csv_cols)
        writer.writeheader()
        writer.writerows(rows)

    # --- JSON (full results) ---
    json_rows = [
        {k: (bool(v) if isinstance(v, (bool, np.bool_)) else
             (float(v) if isinstance(v, (np.floating, float)) else v))
         for k, v in row.items()}
        for row in rows
    ]
    json_path = article_results_dir / "differentiation_test_results.json"
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(json_rows, fh, indent=2)

    # --- Markdown ---
    md_path = article_results_dir / "differentiation_test_results.md"
    header = "| Case | Method | Exact | Approx | Abs Error | Rel Error | Tolerance | Pass |\n"
    separator = "|---|---|---|---|---|---|---|---|\n"
    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write("# 3-Point Numerical Differentiation Results\n\n")
        fh.write(header)
        fh.write(separator)
        for r in rows:
            fh.write(
                f"| {r['case_display']} | {r['method']} "
                f"| {r['exact']:.6e} | {r['approx']:.6e} "
                f"| {r['abs_error']:.3e} | {r['rel_error']:.3e} "
                f"| {r['tolerance']:.0e} | {'Yes' if r['passed'] else 'No'} |\n"
            )

    # --- Summary CSV ---
    summary = build_summary(rows)
    sum_cols = [
        "method", "n_cases", "all_passed",
        "max_abs_error", "mean_abs_error", "max_rel_error", "mean_rel_error",
    ]
    sum_path = article_results_dir / "differentiation_summary.csv"
    with open(sum_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=sum_cols)
        writer.writeheader()
        writer.writerows(summary)

    # --- Run metadata ---
    metadata = {
        "run_index": run_index,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "n_test_cases": len(TEST_CASES),
        "methods": list(METHODS),
        "total_rows": len(rows),
        "all_passed": all(r["passed"] for r in rows),
    }
    meta_path = article_results_dir / "run_metadata.json"
    with open(meta_path, "w", encoding="utf-8") as fh:
        json.dump(metadata, fh, indent=2)

    return csv_path, json_path, md_path, sum_path, meta_path


# ---------------------------------------------------------------------------
# Article image helpers
# ---------------------------------------------------------------------------

def format_cell(value, column_name: str) -> str:
    """Format a table cell value for image rendering."""
    if isinstance(value, (bool, np.bool_)):
        return "Yes" if value else "No"
    if isinstance(value, float) and not isinstance(value, bool):
        return f"{value:.3e}"
    return str(value)


def save_table_image(rows, columns, output_base: Path, title: str):
    """Render a matplotlib table and save as .png and .svg."""
    cell_text = [
        [format_cell(row[col], col) for col in columns]
        for row in rows
    ]
    col_labels = [c.replace("_", " ").title() for c in columns]

    fig_width = max(10, len(columns) * 1.5)
    fig_height = max(2, len(rows) * 0.4 + 1.2)
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.axis("off")
    table = ax.table(
        cellText=cell_text,
        colLabels=col_labels,
        loc="center",
        cellLoc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.auto_set_column_width(list(range(len(columns))))
    ax.set_title(title, fontsize=10, pad=12)
    fig.tight_layout()

    for ext in ("png", "svg"):
        fig.savefig(f"{output_base}.{ext}", dpi=150, bbox_inches="tight")
    plt.close(fig)


def generate_article_images(rows, article_images_dir: Path):
    """Generate summary, full-results, and error-ranking table images."""
    summary = build_summary(rows)

    # Summary table
    sum_cols = [
        "method", "n_cases", "all_passed",
        "max_abs_error", "mean_abs_error", "max_rel_error", "mean_rel_error",
    ]
    save_table_image(
        summary, sum_cols,
        article_images_dir / "summary_table",
        "3-Point Differentiation — Method Summary",
    )

    # All results table
    result_cols = [
        "case_display", "method", "exact", "approx",
        "abs_error", "rel_error", "tolerance", "passed",
    ]
    save_table_image(
        rows, result_cols,
        article_images_dir / "all_results_table",
        "3-Point Differentiation — All Results",
    )

    # Error ranking table (sorted by abs_error ascending)
    ranked = sorted(rows, key=lambda r: r["abs_error"])
    rank_cols = ["case_display", "method", "abs_error", "rel_error", "passed"]
    save_table_image(
        ranked, rank_cols,
        article_images_dir / "error_ranking_table",
        "3-Point Differentiation — Error Ranking (Best to Worst)",
    )

    # Per-case tables
    for case in TEST_CASES:
        case_rows = [r for r in rows if r["case_name"] == case["name"]]
        safe = sanitize_filename(case["name"])
        save_table_image(
            case_rows, result_cols,
            article_images_dir / f"{safe}_results_table",
            f"Results: {case['display']}",
        )


# ---------------------------------------------------------------------------
# Error-vs-h plots
# ---------------------------------------------------------------------------

def generate_plots(tool: DifferentiationTools, plots_dir: Path):
    """Produce log-log error-vs-h plots for each test case."""
    for case in TEST_CASES:
        exact = float(case["df"](case["x"]))
        fig, ax = plt.subplots(figsize=(7, 5))

        for method in METHODS:
            errors = []
            for h in H_VALUES:
                approx = tool.numerical_differentiation_3point(
                    case["f"], case["x"], h=h, method=method
                )
                errors.append(abs(approx - exact))
            ax.loglog(H_VALUES, errors, label=method)

        ax.set_xlabel("Step size h")
        ax.set_ylabel("Absolute error |f'approx − f'exact|")
        ax.set_title(f"Error vs. h — {case['display']}")
        ax.legend()
        ax.grid(True, which="both", ls="--", lw=0.5)
        fig.tight_layout()

        safe = sanitize_filename(case["name"])
        for ext in ("png", "svg"):
            fig.savefig(plots_dir / f"{safe}_error_vs_h.{ext}", dpi=150, bbox_inches="tight")
        plt.close(fig)


# ---------------------------------------------------------------------------
# unittest class
# ---------------------------------------------------------------------------

class TestDifferentiationThreePoint(unittest.TestCase):
    """Unit tests for DifferentiationTools.numerical_differentiation_3point."""

    @classmethod
    def setUpClass(cls):
        cls.tool = DifferentiationTools()
        (
            cls.run_dir,
            cls.article_results_dir,
            cls.plots_dir,
            cls.article_images_dir,
            cls.run_index,
        ) = create_run_output_dirs(PROJECT_ROOT)

        cls.rows = collect_results(cls.tool)
        save_results(cls.rows, cls.article_results_dir, cls.run_index)
        generate_article_images(cls.rows, cls.article_images_dir)
        generate_plots(cls.tool, cls.plots_dir)

        # Write plain-text unit test report
        report_lines = [
            "3-Point Numerical Differentiation — Unit Test Report",
            f"Run index : {cls.run_index}",
            f"Timestamp : {datetime.now(timezone.utc).isoformat()}",
            "",
            f"{'Case':<35} {'Method':<10} {'Abs Err':>12} {'Tol':>10} {'Pass':>6}",
            "-" * 80,
        ]
        for r in cls.rows:
            report_lines.append(
                f"{r['case_display']:<35} {r['method']:<10} "
                f"{r['abs_error']:>12.3e} {r['tolerance']:>10.0e} "
                f"{'Yes' if r['passed'] else 'No':>6}"
            )
        all_pass = all(r["passed"] for r in cls.rows)
        report_lines += ["", f"Overall: {'PASS' if all_pass else 'FAIL'}"]

        report_path = cls.article_results_dir / "unittest_report.txt"
        report_path.write_text("\n".join(report_lines), encoding="utf-8")

    # ------------------------------------------------------------------
    # Tests
    # ------------------------------------------------------------------

    def test_all_methods_meet_tolerance(self):
        """Every (case, method) pair must meet its tolerance."""
        failures = [
            f"{r['case_display']} [{r['method']}]: "
            f"abs_error={r['abs_error']:.3e} > tol={r['tolerance']:.0e}"
            for r in self.rows
            if not r["passed"]
        ]
        self.assertFalse(failures, "Tolerance exceeded:\n" + "\n".join(failures))

    def test_invalid_method_raises_value_error(self):
        """Passing an unknown method name must raise ValueError."""
        with self.assertRaises(ValueError):
            self.tool.numerical_differentiation_3point(np.sin, 1.0, method="secant")

    def test_nonpositive_h_raises_value_error(self):
        """Passing h=0.0 must raise ValueError."""
        with self.assertRaises(ValueError):
            self.tool.numerical_differentiation_3point(np.sin, 1.0, h=0.0)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main(verbosity=2)
