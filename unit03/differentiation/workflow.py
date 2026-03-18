"""Workflow entry points for the differentiation outputs."""

from __future__ import annotations

from typing import Dict

from lib.differentiation_tools import DifferentiationTools

from . import artifacts, calculators, visuals


def generate_all_outputs(tool: DifferentiationTools) -> Dict[str, object]:
    """Run the entire differentiation workflow and return key artifacts."""
    output_root, article_results_dir, plots_dir, article_images_dir = artifacts.create_output_dirs()
    rows = calculators.collect_results(tool)
    freefall_result = calculators.estimate_gravity_from_interpolated_freefall(tool)

    artifacts.save_results(rows, freefall_result)
    visuals.generate_article_images(rows, article_images_dir, freefall_result)
    visuals.generate_plots(tool, plots_dir, freefall_result)
    artifacts.write_unittest_report(rows, freefall_result)

    return {
        "output_root": output_root,
        "article_results_dir": article_results_dir,
        "plots_dir": plots_dir,
        "article_images_dir": article_images_dir,
        "rows": rows,
        "freefall_result": freefall_result,
    }


__all__ = ["generate_all_outputs"]
