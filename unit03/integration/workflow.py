"""Workflow entry points for the integration outputs."""

from __future__ import annotations

from typing import Dict

from lib.integration_tools import IntegrationTools

from . import artifacts, calculators, config, visuals


def generate_all_outputs(tool: IntegrationTools) -> Dict[str, object]:
    """Run both trapezoidal and Simpson workflows and return collected data."""
    article_results_dir, article_images_dir, plots_dir = artifacts.prepare_output_dirs()

    trapezoidal_rows = calculators.collect_method_results(tool, "trapezoidal", tool.composite_trapezoidal)
    simpson_rows = calculators.collect_method_results(tool, "simpson", tool.composite_simpson)

    trapezoidal_summary_rows = calculators.build_summary(
        trapezoidal_rows,
        expected_order=config.TRAPEZOIDAL_ORDER_TARGET,
        tol_key="trap_tol",
    )
    simpson_summary_rows = calculators.build_summary(
        simpson_rows,
        expected_order=config.SIMPSON_ORDER_TARGET,
        tol_key="simp_tol",
    )

    artifacts.write_method_outputs("trapezoidal", trapezoidal_rows, trapezoidal_summary_rows)
    artifacts.write_method_outputs("simpson", simpson_rows, simpson_summary_rows)
    visuals.generate_error_plots(
        "trapezoidal",
        trapezoidal_rows,
        config.TRAPEZOIDAL_ORDER_TARGET,
        plots_dir,
        config.BENCHMARK_CASES,
    )
    visuals.generate_error_plots(
        "simpson",
        simpson_rows,
        config.SIMPSON_ORDER_TARGET,
        plots_dir,
        config.BENCHMARK_CASES,
    )
    visuals.generate_article_images("trapezoidal", trapezoidal_rows, trapezoidal_summary_rows, article_images_dir)
    visuals.generate_article_images("simpson", simpson_rows, simpson_summary_rows, article_images_dir)
    artifacts.write_unittest_report(trapezoidal_summary_rows, simpson_summary_rows)

    return {
        "trapezoidal_rows": trapezoidal_rows,
        "simpson_rows": simpson_rows,
        "trapezoidal_summary_rows": trapezoidal_summary_rows,
        "simpson_summary_rows": simpson_summary_rows,
        "article_results_dir": article_results_dir,
        "article_images_dir": article_images_dir,
        "plots_dir": plots_dir,
    }


__all__ = ["generate_all_outputs"]
