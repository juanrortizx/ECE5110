"""Artifact writers for Unit 03 integration workflows."""

import csv
import json
import shutil
from datetime import datetime, timezone

from .config import ARTICLE_IMAGES_DIR, ARTICLE_RESULTS_DIR, PLOTS_DIR, UNIT_RESULTS_DIR


def prepare_output_dirs(clear_results=True):
    """Clear Unit 03 results and recreate shared output directories."""
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


def _write_csv(path, rows):
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _markdown_table(headers, row_dicts):
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in row_dicts:
        lines.append("| " + " | ".join(str(row[h]) for h in headers) + " |")
    return "\n".join(lines) + "\n"


def write_method_outputs(method_key, rows, summary_rows, metadata):
    """Write method-specific CSV/JSON/Markdown outputs and metadata."""
    results_csv = ARTICLE_RESULTS_DIR / f"integration_{method_key}_results.csv"
    results_json = ARTICLE_RESULTS_DIR / f"integration_{method_key}_results.json"
    results_md = ARTICLE_RESULTS_DIR / f"integration_{method_key}_results.md"
    summary_csv = ARTICLE_RESULTS_DIR / f"integration_{method_key}_summary.csv"
    metadata_json = ARTICLE_RESULTS_DIR / f"integration_{method_key}_metadata.json"

    _write_csv(results_csv, rows)
    _write_csv(summary_csv, summary_rows)
    results_json.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    metadata_json.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    headers = list(rows[0].keys()) if rows else []
    body = "# Integration Results\n\n" + _markdown_table(headers, rows)
    results_md.write_text(body, encoding="utf-8")


def write_unittest_report(method_outputs):
    """Write a unified plain-text report across trapezoidal and Simpson workflows."""
    lines = [
        "Unit 03 Integration Unittest Report",
        "=" * 36,
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
    ]

    for method_key in ("trapezoidal", "simpson"):
        data = method_outputs[method_key]
        lines.append(f"Method: {method_key}")
        lines.append("-" * (8 + len(method_key)))
        for row in data["summary_rows"]:
            lines.append(
                " case={case_name}, n_max={n_max}, final_abs_error={final_abs_error:.6e}, "
                "observed_order={observed_order:.4f}, order_pass={order_pass}".format(**row)
            )
        lines.append(f" all_accuracy_pass={data['all_accuracy_pass']}")
        lines.append(f" all_order_pass={data['all_order_pass']}")
        lines.append("")

    combined = all(
        data["all_accuracy_pass"] and data["all_order_pass"]
        for data in method_outputs.values()
    )
    lines.append(f"Overall combined status: {'PASS' if combined else 'FAIL'}")
    lines.append("")

    path = ARTICLE_RESULTS_DIR / "integration_unittest_report.txt"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
