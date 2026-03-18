"""Workflow orchestration for Unit 03 differentiation outputs."""

from __future__ import annotations

from unit03.differentiation.artifacts import (
    save_results,
    write_unittest_report,
)
from unit03.common.paths import reset_unit_results
from unit03.differentiation.calculators import (
    build_summary,
    collect_results,
    estimate_gravity_from_interpolated_freefall,
)
from unit03.differentiation.visuals import generate_article_images, generate_plots


def generate_all_outputs(tool):
    """Generate all differentiation artifacts, plots, and report content."""
    dirs = reset_unit_results()
    rows = collect_results(tool)
    freefall_result = estimate_gravity_from_interpolated_freefall(tool)

    artifacts_payload = save_results(rows, freefall_result, dirs["article_results_dir"])
    generate_article_images(rows, dirs["article_images_dir"], freefall_result)
    generate_plots(tool, dirs["plots_dir"], freefall_result)
    report_path = write_unittest_report(rows, freefall_result, dirs["article_results_dir"])

    return {
        "rows": rows,
        "summary": build_summary(rows),
        "freefall_result": freefall_result,
        "artifact_payload": artifacts_payload,
        "output_dirs": dirs,
        "report_path": report_path,
    }
