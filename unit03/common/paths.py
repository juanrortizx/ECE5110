"""Shared path constants and output-directory setup for Unit 03."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
UNIT_RESULTS_DIR = PROJECT_ROOT / "unit03" / "results"
ARTICLE_RESULTS_DIR = UNIT_RESULTS_DIR / "article_results"
PLOTS_DIR = UNIT_RESULTS_DIR / "plots"
ARTICLE_IMAGES_DIR = UNIT_RESULTS_DIR / "article_images"


def reset_unit_results():
    """Ensure Unit 03 result directories exist.

    Returns
    -------
    dict
        Dictionary with absolute paths for result directories.
    """
    ARTICLE_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    ARTICLE_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    return {
        "unit_results_dir": UNIT_RESULTS_DIR,
        "article_results_dir": ARTICLE_RESULTS_DIR,
        "plots_dir": PLOTS_DIR,
        "article_images_dir": ARTICLE_IMAGES_DIR,
    }
