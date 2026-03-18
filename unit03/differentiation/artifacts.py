"""Artifact generation utilities for Unit 03 differentiation."""

from __future__ import annotations

from datetime import datetime, timezone

from unit03.common.artifact_io import (
    markdown_table_formatted,
    write_csv,
    write_json,
    write_text,
)
from unit03.differentiation.calculators import build_summary


def sanitize_filename(text):
    """Convert arbitrary labels into filesystem-friendly lowercase stems."""
    slug = []
    for char in text.lower():
        slug.append(char if char.isalnum() else "_")
    return "".join(slug).strip("_")


def save_results(rows, freefall_result, article_results_dir):
    """Write all differentiation CSV/JSON/Markdown outputs."""
    summary_rows = build_summary(rows)
    timestamp = datetime.now(timezone.utc).isoformat()
    metadata = {
        "generated_utc": timestamp,
        "workflow": "unit03.differentiation",
        "total_rows": len(rows),
        "all_analytic_passed": all(row["passed"] for row in rows),
        "freefall_passed": bool(freefall_result["passed"]),
    }

    result_headers = [
        "case",
        "case_display",
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
    summary_headers = [
        "method",
        "passed",
        "failed",
        "total",
        "max_abs_error",
        "mean_abs_error",
        "max_rel_error",
        "mean_rel_error",
    ]

    ranking_rows = sorted(rows, key=lambda row: row["abs_error"], reverse=True)
    freefall_table_rows = [
        {
            "step_size": freefall_result["step_size"],
            "evaluation_time": freefall_result["evaluation_time"],
            "acceleration_signed": freefall_result["acceleration_signed"],
            "acceleration_magnitude": freefall_result["acceleration_magnitude"],
            "target_abs_gravity": freefall_result["target_abs_gravity"],
            "absolute_error": freefall_result["absolute_error"],
            "tolerance": freefall_result["tolerance"],
            "passed": freefall_result["passed"],
        }
    ]

    write_csv(article_results_dir / "differentiation_test_results.csv", rows, result_headers)
    write_json(article_results_dir / "differentiation_test_results.json", rows)
    write_text(
        article_results_dir / "differentiation_test_results.md",
        markdown_table_formatted(rows, result_headers, float_sigfigs=8),
    )

    write_csv(
        article_results_dir / "differentiation_summary.csv",
        summary_rows,
        summary_headers,
    )
    write_json(article_results_dir / "differentiation_summary.json", summary_rows)
    write_text(
        article_results_dir / "differentiation_summary.md",
        markdown_table_formatted(summary_rows, summary_headers, float_sigfigs=8),
    )

    write_csv(
        article_results_dir / "differentiation_error_ranking.csv",
        ranking_rows,
        result_headers,
    )

    write_json(article_results_dir / "run_metadata.json", metadata)

    freefall_headers = list(freefall_table_rows[0].keys())
    write_csv(
        article_results_dir / "freefall_gravity_results.csv",
        freefall_table_rows,
        freefall_headers,
    )
    write_json(
        article_results_dir / "freefall_gravity_results.json",
        freefall_result,
    )
    write_text(
        article_results_dir / "freefall_gravity_results.md",
        markdown_table_formatted(freefall_table_rows, freefall_headers, float_sigfigs=8),
    )

    coeff_rows = [
        {"index": idx, "coefficient": value}
        for idx, value in enumerate(freefall_result["coefficients"])
    ]
    write_csv(
        article_results_dir / "differentiation_freefall_coefficients.csv",
        coeff_rows,
        ["index", "coefficient"],
    )

    return {
        "summary_rows": summary_rows,
        "metadata": metadata,
        "ranking_rows": ranking_rows,
    }


def write_unittest_report(rows, freefall_result, article_results_dir):
    """Write plain-text report summarizing analytic and gravity checks."""
    analytic_pass = all(row["passed"] for row in rows)
    gravity_pass = bool(freefall_result["passed"])
    combined_pass = analytic_pass and gravity_pass

    report = [
        "Unit 03 Differentiation Unittest Report",
        "=" * 40,
        "",
        "Analytic checks:",
        f"- Total checks: {len(rows)}",
        f"- Passed: {sum(1 for row in rows if row['passed'])}",
        f"- Failed: {sum(1 for row in rows if not row['passed'])}",
        f"- Overall analytic status: {'PASS' if analytic_pass else 'FAIL'}",
        "",
        "Gravity validation:",
        f"- Evaluation time: {freefall_result['evaluation_time']:.6f} s",
        f"- Estimated signed acceleration: {freefall_result['acceleration_signed']:.8f} m/s^2",
        f"- Acceleration magnitude: {freefall_result['acceleration_magnitude']:.8f} m/s^2",
        f"- Target |g|: {freefall_result['target_abs_gravity']:.3f} m/s^2",
        f"- Magnitude absolute error: {freefall_result['absolute_error']:.8f}",
        f"- Tolerance: {freefall_result['tolerance']:.3f}",
        f"- Gravity status: {'PASS' if gravity_pass else 'FAIL'}",
        "",
        f"Overall combined status: {'PASS' if combined_pass else 'FAIL'}",
    ]

    report_path = article_results_dir / "unittest_report.txt"
    write_text(report_path, "\n".join(report))
    return report_path
