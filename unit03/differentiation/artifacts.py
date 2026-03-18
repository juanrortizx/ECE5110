"""Artifact export helpers for Unit 03 differentiation workflow."""

from datetime import datetime, timezone

from unit03.common.artifact_io import format_sci, write_csv, write_json, write_markdown_table, write_text
from unit03.differentiation.calculators import build_summary


def sanitize_filename(name):
    return "".join(ch if (ch.isalnum() or ch == "_") else "_" for ch in name.lower())


def _render_rows_for_markdown(rows):
    rendered = []
    for row in rows:
        rendered_row = {}
        for key, value in row.items():
            rendered_row[key] = format_sci(value)
        rendered.append(rendered_row)
    return rendered


def save_results(rows, freefall_result, article_results_dir):
    summary = build_summary(rows)
    ranking = sorted(rows, key=lambda row: row["abs_error"], reverse=True)

    result_headers = [
        "case_name",
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
        "total_cases",
        "pass_count",
        "fail_count",
        "max_abs_error",
        "mean_abs_error",
        "max_rel_error",
        "mean_rel_error",
    ]

    write_csv(rows, result_headers, article_results_dir / "differentiation_test_results.csv")
    write_json(rows, article_results_dir / "differentiation_test_results.json")
    write_markdown_table(
        _render_rows_for_markdown(rows),
        result_headers,
        article_results_dir / "differentiation_test_results.md",
    )

    write_csv(summary, summary_headers, article_results_dir / "differentiation_summary.csv")
    write_json(summary, article_results_dir / "differentiation_summary.json")
    write_markdown_table(
        _render_rows_for_markdown(summary),
        summary_headers,
        article_results_dir / "differentiation_summary.md",
    )

    ranking_headers = ["case_name", "method", "abs_error", "rel_error", "passed"]
    write_csv(ranking, ranking_headers, article_results_dir / "differentiation_error_ranking.csv")

    coeff_rows = [
        {
            "coefficient_index": int(index),
            "coefficient_value": float(value),
        }
        for index, value in enumerate(freefall_result["poly_coefficients"])
    ]
    write_csv(
        coeff_rows,
        ["coefficient_index", "coefficient_value"],
        article_results_dir / "differentiation_freefall_coefficients.csv",
    )

    freefall_rows = [
        {
            "evaluation_time": freefall_result["evaluation_time"],
            "estimated_accel_signed": freefall_result["estimated_accel_signed"],
            "estimated_accel_magnitude": freefall_result["estimated_accel_magnitude"],
            "target_gravity_magnitude": freefall_result["target_gravity_magnitude"],
            "magnitude_abs_error": freefall_result["magnitude_abs_error"],
            "tolerance": freefall_result["tolerance"],
            "passed": freefall_result["passed"],
        }
    ]
    freefall_headers = [
        "evaluation_time",
        "estimated_accel_signed",
        "estimated_accel_magnitude",
        "target_gravity_magnitude",
        "magnitude_abs_error",
        "tolerance",
        "passed",
    ]
    write_csv(freefall_rows, freefall_headers, article_results_dir / "freefall_gravity_results.csv")
    write_json(freefall_result, article_results_dir / "freefall_gravity_results.json")
    write_markdown_table(
        _render_rows_for_markdown(freefall_rows),
        freefall_headers,
        article_results_dir / "freefall_gravity_results.md",
    )

    metadata = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "analytic_case_count": len(rows),
        "all_analytic_passed": all(row["passed"] for row in rows),
        "freefall_passed": bool(freefall_result["passed"]),
        "overall_passed": bool(all(row["passed"] for row in rows) and freefall_result["passed"]),
    }
    write_json(metadata, article_results_dir / "run_metadata.json")

    return {
        "summary": summary,
        "ranking": ranking,
        "metadata": metadata,
    }


def write_unittest_report(rows, freefall_result, article_results_dir):
    analytic_pass = all(row["passed"] for row in rows)
    gravity_pass = bool(freefall_result["passed"])
    combined_pass = analytic_pass and gravity_pass

    lines = []
    lines.append("Unit 03 Differentiation Unittest Report")
    lines.append("=" * 40)
    lines.append("")
    lines.append("Analytic case summary")
    lines.append("case_name,method,abs_error,tolerance,passed")

    for row in rows:
        lines.append(
            f"{row['case_name']},{row['method']},{row['abs_error']:.8e},{row['tolerance']:.8e},{row['passed']}"
        )

    lines.append("")
    lines.append("Gravity check summary")
    lines.append(f"evaluation_time={freefall_result['evaluation_time']:.8e}")
    lines.append(f"estimated_signed_acceleration={freefall_result['estimated_accel_signed']:.8e}")
    lines.append(f"acceleration_magnitude={freefall_result['estimated_accel_magnitude']:.8e}")
    lines.append(f"target_g_magnitude={freefall_result['target_gravity_magnitude']:.8e}")
    lines.append(f"magnitude_absolute_error={freefall_result['magnitude_abs_error']:.8e}")
    lines.append(f"tolerance={freefall_result['tolerance']:.8e}")
    lines.append(f"gravity_pass={gravity_pass}")
    lines.append(f"overall_analytic_status={analytic_pass}")
    lines.append(f"overall_gravity_status={gravity_pass}")
    lines.append(f"overall_combined_status={combined_pass}")
    lines.append("")

    write_text("\n".join(lines), article_results_dir / "unittest_report.txt")
