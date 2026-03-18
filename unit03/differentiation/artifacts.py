"""Artifact writers for Unit 03 differentiation workflow."""

import csv
import json
import re
import shutil
from datetime import datetime, timezone

from .calculators import build_summary
from .config import ARTICLE_RESULTS_DIR, ARTICLE_IMAGES_DIR, PLOTS_DIR, UNIT_RESULTS_DIR


def create_output_dirs(clear_results=True):
    """Clear Unit 03 results and recreate expected output directories."""
    if clear_results and UNIT_RESULTS_DIR.exists():
        shutil.rmtree(UNIT_RESULTS_DIR)

    ARTICLE_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    ARTICLE_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    return {
        "unit_results": UNIT_RESULTS_DIR,
        "article_results": ARTICLE_RESULTS_DIR,
        "plots": PLOTS_DIR,
        "article_images": ARTICLE_IMAGES_DIR,
    }


def sanitize_filename(name):
    """Normalize a filename stem to lowercase snake case."""
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "_", name.strip().lower())
    return re.sub(r"_+", "_", cleaned).strip("_")


def format_cell(value):
    """Format table cells consistently for markdown and text outputs."""
    if isinstance(value, bool):
        return "PASS" if value else "FAIL"
    if isinstance(value, float):
        return f"{value:.10g}"
    return str(value)


def _markdown_table(headers, row_dicts):
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in row_dicts:
        lines.append("| " + " | ".join(format_cell(row[h]) for h in headers) + " |")
    return "\n".join(lines) + "\n"


def _write_csv(path, rows):
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def save_results(rows, freefall_result):
    """Write differentiation CSV/JSON/Markdown outputs and metadata."""
    summary_rows = build_summary(rows)

    diff_csv = ARTICLE_RESULTS_DIR / "differentiation_test_results.csv"
    diff_json = ARTICLE_RESULTS_DIR / "differentiation_test_results.json"
    diff_md = ARTICLE_RESULTS_DIR / "differentiation_test_results.md"
    summary_csv = ARTICLE_RESULTS_DIR / "differentiation_summary.csv"

    freefall_csv = ARTICLE_RESULTS_DIR / "freefall_gravity_results.csv"
    freefall_json = ARTICLE_RESULTS_DIR / "freefall_gravity_results.json"
    freefall_md = ARTICLE_RESULTS_DIR / "freefall_gravity_results.md"

    _write_csv(diff_csv, rows)
    _write_csv(summary_csv, summary_rows)
    _write_csv(freefall_csv, [freefall_result])

    diff_json.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    freefall_json.write_text(json.dumps(freefall_result, indent=2), encoding="utf-8")

    diff_headers = list(rows[0].keys()) if rows else []
    diff_md.write_text(
        "# Differentiation Test Results\n\n" + _markdown_table(diff_headers, rows),
        encoding="utf-8",
    )

    freefall_lines = [
        "# Free-Fall Gravity Validation\n",
        "## Gravity Check Summary\n",
        _markdown_table(list(freefall_result.keys()), [freefall_result]),
        "## Source Data\n",
    ]
    source_rows = [
        {"time_s": t, "position_m": y}
        for t, y in zip(
            freefall_result["source_time_data"],
            freefall_result["source_position_data"],
        )
    ]
    freefall_lines.append(_markdown_table(["time_s", "position_m"], source_rows))
    freefall_md.write_text("\n".join(freefall_lines), encoding="utf-8")

    run_metadata = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "analytic_total_rows": len(rows),
        "analytic_all_pass": all(r["pass"] for r in rows),
        "gravity_pass": bool(freefall_result["pass"]),
        "combined_pass": bool(all(r["pass"] for r in rows) and freefall_result["pass"]),
    }
    (ARTICLE_RESULTS_DIR / "run_metadata.json").write_text(
        json.dumps(run_metadata, indent=2),
        encoding="utf-8",
    )

    return {
        "rows": rows,
        "summary_rows": summary_rows,
        "freefall_result": freefall_result,
        "metadata": run_metadata,
    }


def write_unittest_report(rows, freefall_result):
    """Write plain-text unittest report for analytic and gravity checks."""
    summary_rows = build_summary(rows)
    analytic_pass = all(r["pass"] for r in rows)
    gravity_pass = bool(freefall_result["pass"])
    combined_pass = analytic_pass and gravity_pass

    lines = [
        "Unit 03 Differentiation Unittest Report",
        "=" * 40,
        "",
        "Analytic Summary:",
    ]
    for row in summary_rows:
        lines.append(
            " - {method}: pass={pass_count}/{num_cases}, max_abs_error={max_abs_error:.6e}, "
            "mean_abs_error={mean_abs_error:.6e}, all_pass={all_pass}".format(**row)
        )

    lines.extend(
        [
            "",
            "Gravity Check:",
            f" - evaluation time (s): {freefall_result['evaluation_time']:.6f}",
            f" - estimated signed acceleration (m/s^2): {freefall_result['acceleration_signed']:.8f}",
            f" - acceleration magnitude |a| (m/s^2): {freefall_result['acceleration_magnitude']:.8f}",
            f" - target |g| (m/s^2): {freefall_result['target_gravity_magnitude']:.8f}",
            f" - | |a| - |g| |: {freefall_result['magnitude_abs_error']:.8f}",
            f" - tolerance: {freefall_result['tolerance']:.6f}",
            f" - pass: {freefall_result['pass']}",
            "",
            f"Overall analytic status: {'PASS' if analytic_pass else 'FAIL'}",
            f"Overall gravity status: {'PASS' if gravity_pass else 'FAIL'}",
            f"Overall combined status: {'PASS' if combined_pass else 'FAIL'}",
            "",
        ]
    )

    report_path = ARTICLE_RESULTS_DIR / "unittest_report.txt"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path
