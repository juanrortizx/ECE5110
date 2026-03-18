"""Top-level orchestration for Unit 03 differentiation workflow."""

from unit03.common.paths import reset_unit_results
from unit03.differentiation.artifacts import save_results, write_unittest_report
from unit03.differentiation.calculators import collect_results, estimate_gravity_from_interpolated_freefall
from unit03.differentiation.visuals import generate_article_images, generate_plots


def generate_all_outputs(tool):
    paths = reset_unit_results()
    article_results_dir = paths["article_results_dir"]
    plots_dir = paths["plots_dir"]
    article_images_dir = paths["article_images_dir"]

    rows = collect_results(tool)
    freefall_result = estimate_gravity_from_interpolated_freefall(tool)
    artifact_data = save_results(rows, freefall_result, article_results_dir)

    generate_article_images(rows, article_images_dir, freefall_result)
    generate_plots(tool, plots_dir, freefall_result)
    write_unittest_report(rows, freefall_result, article_results_dir)

    return {
        "rows": rows,
        "summary": artifact_data["summary"],
        "ranking": artifact_data["ranking"],
        "metadata": artifact_data["metadata"],
        "freefall_result": freefall_result,
    }
