"""Top-level orchestration for Unit 03 integration workflow."""

from unit03.common.paths import reset_unit_results
from unit03.integration.artifacts import write_method_outputs, write_unittest_report
from unit03.integration.calculators import build_summary, collect_method_results
from unit03.integration.visuals import generate_article_images, generate_error_plots


def generate_all_outputs(tool):
    paths = reset_unit_results()
    article_results_dir = paths["article_results_dir"]
    plots_dir = paths["plots_dir"]
    article_images_dir = paths["article_images_dir"]

    trapezoidal_rows = collect_method_results(tool, "trapezoidal")
    trapezoidal_summary = build_summary(trapezoidal_rows)

    simpson_rows = collect_method_results(tool, "simpson")
    simpson_summary = build_summary(simpson_rows)

    write_method_outputs("trapezoidal", trapezoidal_rows, trapezoidal_summary, article_results_dir)
    write_method_outputs("simpson", simpson_rows, simpson_summary, article_results_dir)
    write_unittest_report(trapezoidal_summary, simpson_summary, article_results_dir)

    generate_article_images("trapezoidal", trapezoidal_rows, trapezoidal_summary, article_images_dir)
    generate_article_images("simpson", simpson_rows, simpson_summary, article_images_dir)
    generate_error_plots("trapezoidal", trapezoidal_rows, plots_dir)
    generate_error_plots("simpson", simpson_rows, plots_dir)

    return {
        "trapezoidal": {"rows": trapezoidal_rows, "summary": trapezoidal_summary},
        "simpson": {"rows": simpson_rows, "summary": simpson_summary},
    }
