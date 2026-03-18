"""Artifact export helpers for Unit 03 integration workflow."""

from datetime import datetime, timezone

from unit03.common.artifact_io import format_sci, write_csv, write_json, write_markdown_table, write_text


def _rows_for_markdown(rows):
    out = []
    for row in rows:
        out.append({key: format_sci(value) for key, value in row.items()})
    return out


def write_method_outputs(method_key, rows, summary_rows, article_results_dir):
    results_headers = [
        "method",
        "case_name",
        "case_display",
        "a",
        "b",
        "n",
        "h",
        "exact",
        "approx",
        "abs_error",
    ]
    summary_headers = [
        "method",
        "case_name",
        "min_abs_error",
        "max_abs_error",
        "final_n",
        "final_abs_error",
        "observed_order",
    ]

    write_csv(rows, results_headers, article_results_dir / f"integration_{method_key}_results.csv")
    write_json(rows, article_results_dir / f"integration_{method_key}_results.json")
    write_markdown_table(
        _rows_for_markdown(rows),
        results_headers,
        article_results_dir / f"integration_{method_key}_results.md",
    )

    write_csv(summary_rows, summary_headers, article_results_dir / f"integration_{method_key}_summary.csv")
    write_json(summary_rows, article_results_dir / f"integration_{method_key}_summary.json")
    write_markdown_table(
        _rows_for_markdown(summary_rows),
        summary_headers,
        article_results_dir / f"integration_{method_key}_summary.md",
    )

    metadata = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "method": method_key,
        "row_count": len(rows),
        "summary_count": len(summary_rows),
    }
    write_json(metadata, article_results_dir / f"integration_{method_key}_metadata.json")


def write_unittest_report(trapezoidal_summary, simpson_summary, article_results_dir):
    lines = []
    lines.append("Unit 03 Integration Unittest Report")
    lines.append("=" * 36)
    lines.append("")
    lines.append("Trapezoidal summary")
    lines.append("case_name,observed_order,final_abs_error")
    for row in trapezoidal_summary:
        lines.append(f"{row['case_name']},{row['observed_order']:.8f},{row['final_abs_error']:.8e}")

    lines.append("")
    lines.append("Simpson summary")
    lines.append("case_name,observed_order,final_abs_error")
    for row in simpson_summary:
        lines.append(f"{row['case_name']},{row['observed_order']:.8f},{row['final_abs_error']:.8e}")

    write_text("\n".join(lines) + "\n", article_results_dir / "integration_unittest_report.txt")
