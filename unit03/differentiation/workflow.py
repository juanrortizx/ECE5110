"""Orchestration for Unit 03 differentiation outputs."""

from .artifacts import create_output_dirs, save_results, write_unittest_report
from .calculators import collect_results, estimate_gravity_from_interpolated_freefall
from .visuals import generate_article_images, generate_plots


def generate_all_outputs(tool, clear_results=True):
    """Run the full differentiation workflow and return generated data."""
    output_dirs = create_output_dirs(clear_results=clear_results)
    rows = collect_results(tool)
    freefall_result = estimate_gravity_from_interpolated_freefall(tool, h=1e-4)

    saved = save_results(rows, freefall_result)
    generate_article_images(rows, output_dirs["article_images"], freefall_result)
    generate_plots(tool, output_dirs["plots"], freefall_result)
    report_path = write_unittest_report(rows, freefall_result)

    return {
        "rows": saved["rows"],
        "summary_rows": saved["summary_rows"],
        "freefall_result": saved["freefall_result"],
        "metadata": saved["metadata"],
        "output_dirs": output_dirs,
        "report_path": report_path,
    }
