"""Workflow orchestrator for Unit 03 integration outputs."""

from __future__ import annotations

from unit03.integration.artifacts import (
    write_method_outputs,
    write_unittest_report,
)
from unit03.common.paths import reset_unit_results
from unit03.integration.calculators import build_summary, collect_method_results
from unit03.integration.config import EXPECTED_ORDER, METHODS, MIN_OBSERVED_ORDER
from unit03.integration.visuals import generate_article_images, generate_error_plots


def generate_all_outputs(tool):
    """Generate all integration artifacts for trapezoidal and Simpson rules."""
    dirs = reset_unit_results()
    payload_by_method = {}

    for method in METHODS:
        rows = collect_method_results(tool, method)
        summary_rows = build_summary(rows)
        order_checks = [
            row["observed_order"] >= MIN_OBSERVED_ORDER[method] for row in summary_rows
        ]
        metadata = write_method_outputs(
            method,
            rows,
            summary_rows,
            dirs["article_results_dir"],
            EXPECTED_ORDER[method],
        )
        generate_article_images(method, rows, summary_rows, dirs["article_images_dir"])
        generate_error_plots(method, rows, dirs["plots_dir"])
        payload_by_method[method] = {
            "rows": rows,
            "summary_rows": summary_rows,
            "order_checks": order_checks,
            "metadata": metadata,
        }

    report_path = write_unittest_report(payload_by_method, dirs["article_results_dir"])
    return {
        "output_dirs": dirs,
        "methods": payload_by_method,
        "report_path": report_path,
    }
