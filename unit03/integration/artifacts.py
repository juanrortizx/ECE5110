"""Output helpers for Unit 03 integration workflows."""

from __future__ import annotations

import csv
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Sequence

import numpy as np

from .config import (
    ARTICLE_IMAGES_DIR,
    ARTICLE_RESULTS_DIR,
    BENCHMARK_CASES,
    N_VALUES,
    UNIT_RESULTS_DIR,
)


def prepare_output_dirs():
    """Clear and recreate the shared Unit 03 output directories."""
    if UNIT_RESULTS_DIR.exists():
        shutil.rmtree(UNIT_RESULTS_DIR)

    ARTICLE_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    ARTICLE_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    plots_dir = UNIT_RESULTS_DIR / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)
    return ARTICLE_RESULTS_DIR, ARTICLE_IMAGES_DIR, plots_dir


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


def write_unittest_report(trapezoidal_summary_rows, simpson_summary_rows):
    lines = [
        "Unit 03 Integration Report",
        "=" * 26,
        "",
        "Benchmarks:",
    ]

    for case in BENCHMARK_CASES:
        lines.append(f"- {case['case_name']}: {case['display_name']} (exact = {float(case['exact']):.12f})")

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


__all__ = [
    "prepare_output_dirs",
    "format_cell",
    "markdown_table",
    "sanitize_filename",
    "write_method_outputs",
    "write_unittest_report",
]
