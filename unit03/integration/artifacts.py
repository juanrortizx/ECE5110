"""Artifact output helpers for Unit 03 integration workflows."""

from __future__ import annotations

from datetime import datetime, timezone

from unit03.common.artifact_io import markdown_table_formatted, write_csv, write_json, write_text


def write_method_outputs(method, rows, summary_rows, article_results_dir, expected_order):
    """Write per-method CSV/JSON/Markdown outputs and metadata."""
    result_cols = [
        "method",
        "case",
        "case_display",
        "a",
        "b",
        "n",
        "h",
        "exact",
        "approx",
        "abs_error",
        "rel_error",
    ]
    summary_cols = [
        "method",
        "case",
        "case_display",
        "observed_order",
        "best_n",
        "best_abs_error",
        "final_n",
        "final_abs_error",
    ]

    stem = f"integration_{method}"
    write_csv(article_results_dir / f"{stem}_results.csv", rows, result_cols)
    write_json(article_results_dir / f"{stem}_results.json", rows)
    write_text(
        article_results_dir / f"{stem}_results.md",
        markdown_table_formatted(rows, result_cols, float_sigfigs=10),
    )

    write_csv(article_results_dir / f"{stem}_summary.csv", summary_rows, summary_cols)
    write_json(article_results_dir / f"{stem}_summary.json", summary_rows)
    write_text(
        article_results_dir / f"{stem}_summary.md",
        markdown_table_formatted(summary_rows, summary_cols, float_sigfigs=10),
    )

    metadata = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "method": method,
        "expected_order": expected_order,
        "row_count": len(rows),
        "summary_count": len(summary_rows),
    }
    write_json(article_results_dir / f"{stem}_metadata.json", metadata)
    return metadata


def write_unittest_report(payload_by_method, article_results_dir):
    """Write plain-text unittest summary spanning both integration methods."""
    lines = ["Unit 03 Integration Unittest Report", "=" * 36, ""]
    all_ok = True

    for method, payload in payload_by_method.items():
        lines.append(f"Method: {method}")
        for row in payload["summary_rows"]:
            order = row["observed_order"]
            order_text = f"{order:.6f}" if order == order else "nan"
            lines.append(
                "- "
                f"{row['case_display']}: observed_order={order_text}, "
                f"best_abs_error={row['best_abs_error']:.6e}, final_n={row['final_n']}"
            )
        method_ok = all(payload["order_checks"])
        all_ok = all_ok and method_ok
        lines.append(f"- Order status: {'PASS' if method_ok else 'FAIL'}")
        lines.append("")

    lines.append(f"Overall integration status: {'PASS' if all_ok else 'FAIL'}")
    report_path = article_results_dir / "integration_unittest_report.txt"
    write_text(report_path, "\n".join(lines))
    return report_path
