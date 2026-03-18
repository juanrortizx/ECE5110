"""File-system helpers for differentiation outputs."""

from __future__ import annotations

import csv
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, Sequence

import numpy as np

from .calculators import build_summary
from .config import (
    ARTICLE_RESULTS_DIR,
    H_VALUES,
    METHODS,
    TEST_CASES,
    UNIT_RESULTS_DIR,
)


def create_output_dirs():
    """Clear and recreate the Unit 03 output folder structure."""
    if UNIT_RESULTS_DIR.exists():
        shutil.rmtree(UNIT_RESULTS_DIR)

    ARTICLE_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    plots_dir = UNIT_RESULTS_DIR / "plots"
    article_images_dir = UNIT_RESULTS_DIR / "article_images"
    plots_dir.mkdir(parents=True, exist_ok=True)
    article_images_dir.mkdir(parents=True, exist_ok=True)
    return UNIT_RESULTS_DIR, ARTICLE_RESULTS_DIR, plots_dir, article_images_dir


def sanitize_filename(name: str) -> str:
    """Produce lowercase filenames with underscores for unsafe characters."""
    cleaned = []
    previous_was_underscore = False

    for char in name.lower():
        if char.isalnum():
            cleaned.append(char)
            previous_was_underscore = False
        elif not previous_was_underscore:
            cleaned.append("_")
            previous_was_underscore = True

    sanitized = "".join(cleaned).strip("_")
    return sanitized or "table"


def format_cell(value, column_name=None):
    """Format table cell content uniformly."""
    _ = column_name
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, (int, np.integer)):
        return str(int(value))
    if isinstance(value, (float, np.floating)):
        return f"{float(value):.6e}"
    return str(value)


def _markdown_table(rows: Sequence[Dict[str, object]], columns: Sequence[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    data_lines = []

    for row in rows:
        cells = [format_cell(row[col], col) for col in columns]
        data_lines.append("| " + " | ".join(cells) + " |")

    return "\n".join([header, separator] + data_lines)


def save_results(rows: Sequence[Dict[str, object]], freefall_result: Dict[str, object]):
    """Save CSV/JSON/Markdown outputs for analytic and free-fall results."""
    result_columns = [
        "case_name",
        "display_name",
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
    summary = build_summary(rows)
    summary_columns = [
        "method",
        "num_cases",
        "all_passed",
        "max_abs_error",
        "mean_abs_error",
        "max_rel_error",
        "mean_rel_error",
    ]

    results_csv = ARTICLE_RESULTS_DIR / "differentiation_test_results.csv"
    with results_csv.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=result_columns)
        writer.writeheader()
        writer.writerows(rows)

    results_json = ARTICLE_RESULTS_DIR / "differentiation_test_results.json"
    with results_json.open("w", encoding="utf-8") as file:
        json.dump(rows, file, indent=2)

    results_md = ARTICLE_RESULTS_DIR / "differentiation_test_results.md"
    with results_md.open("w", encoding="utf-8") as file:
        file.write("# 3-Point Differentiation Test Results\n\n")
        file.write(_markdown_table(rows, result_columns) + "\n")

    summary_csv = ARTICLE_RESULTS_DIR / "differentiation_summary.csv"
    with summary_csv.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=summary_columns)
        writer.writeheader()
        writer.writerows(summary)

    freefall_columns = [
        "case_name",
        "display_name",
        "interpolant_type",
        "evaluation_time",
        "step_size",
        "accel_estimate_signed",
        "accel_estimate_magnitude",
        "target_gravity_magnitude",
        "magnitude_abs_error",
        "tolerance",
        "passed",
        "time_units",
        "position_units",
        "acceleration_units",
    ]
    freefall_row = {column: freefall_result[column] for column in freefall_columns}

    freefall_csv = ARTICLE_RESULTS_DIR / "freefall_gravity_results.csv"
    with freefall_csv.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=freefall_columns)
        writer.writeheader()
        writer.writerow(freefall_row)

    freefall_json = ARTICLE_RESULTS_DIR / "freefall_gravity_results.json"
    with freefall_json.open("w", encoding="utf-8") as file:
        json.dump(freefall_result, file, indent=2)

    freefall_md = ARTICLE_RESULTS_DIR / "freefall_gravity_results.md"
    with freefall_md.open("w", encoding="utf-8") as file:
        file.write("# Free-Fall Gravity Validation\n\n")
        file.write(
            "This result uses a quadratic interpolant of position-versus-time data, then applies "
            "the central 3-point finite-difference method twice (position -> velocity -> acceleration).\n\n"
        )
        file.write("## Gravity Estimate Summary\n\n")
        file.write(_markdown_table([freefall_row], freefall_columns) + "\n\n")
        file.write("## Source Data\n\n")
        source_rows = [
            {
                "index": idx,
                "time_s": freefall_result["source_time_data"][idx],
                "position_m": freefall_result["source_position_data"][idx],
            }
            for idx in range(len(freefall_result["source_time_data"]))
        ]
        file.write(_markdown_table(source_rows, ["index", "time_s", "position_m"]) + "\n\n")
        file.write("## Quadratic Interpolant Coefficients\n\n")
        coeff_rows = [
            {"coefficient": f"a{2 - idx}", "value": value}
            for idx, value in enumerate(freefall_result["quadratic_coefficients"])
        ]
        file.write(_markdown_table(coeff_rows, ["coefficient", "value"]) + "\n")

    metadata = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "num_analytic_cases": len(TEST_CASES),
        "num_analytic_rows": len(rows),
        "methods": list(METHODS),
        "h_values": H_VALUES.tolist(),
        "output_root": str(UNIT_RESULTS_DIR),
        "gravity_case_name": freefall_result["case_name"],
        "gravity_passed": bool(freefall_result["passed"]),
    }
    metadata_json = ARTICLE_RESULTS_DIR / "run_metadata.json"
    with metadata_json.open("w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2)


def write_unittest_report(rows: Sequence[Dict[str, object]], freefall_result: Dict[str, object]):
    """Write a plain-text summary mirroring unittest expectations."""
    summary_rows = build_summary(rows)

    analytic_ok = all(row["passed"] for row in rows)
    gravity_ok = bool(freefall_result["passed"])
    overall_ok = analytic_ok and gravity_ok

    lines = [
        "Unit 03 Differentiation Report",
        "=" * 34,
        "",
        "Analytic Summary (per method):",
        "method | num_cases | all_passed | max_abs_error | mean_abs_error | max_rel_error | mean_rel_error",
    ]

    for row in summary_rows:
        lines.append(
            "{method} | {num_cases} | {all_passed} | {max_abs_error:.6e} | {mean_abs_error:.6e} | "
            "{max_rel_error:.6e} | {mean_rel_error:.6e}".format(**row)
        )

    lines.extend(
        [
            "",
            "Gravity Check Summary:",
            f"evaluation_time_s: {freefall_result['evaluation_time']:.6e}",
            f"estimated_signed_accel_mps2: {freefall_result['accel_estimate_signed']:.6e}",
            f"estimated_accel_magnitude_mps2: {freefall_result['accel_estimate_magnitude']:.6e}",
            f"target_abs_g_mps2: {freefall_result['target_gravity_magnitude']:.6e}",
            f"magnitude_abs_error: {freefall_result['magnitude_abs_error']:.6e}",
            f"tolerance: {freefall_result['tolerance']:.6e}",
            f"pass: {freefall_result['passed']}",
            "",
            f"overall_analytic_status: {analytic_ok}",
            f"overall_gravity_status: {gravity_ok}",
            f"overall_combined_status: {overall_ok}",
            "",
        ]
    )

    report_path = ARTICLE_RESULTS_DIR / "unittest_report.txt"
    report_path.write_text("\n".join(lines), encoding="utf-8")


__all__ = [
    "create_output_dirs",
    "sanitize_filename",
    "format_cell",
    "save_results",
    "write_unittest_report",
]
