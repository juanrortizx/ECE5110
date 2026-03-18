"""Shared path constants and output-directory setup for Unit 03."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
UNIT_RESULTS_DIR = PROJECT_ROOT / "unit03" / "results"
ARTICLE_RESULTS_DIR = UNIT_RESULTS_DIR / "article_results"
PLOTS_DIR = UNIT_RESULTS_DIR / "plots"
ARTICLE_IMAGES_DIR = UNIT_RESULTS_DIR / "article_images"


def reset_unit_results():
    """Ensure required Unit 03 output directories exist.

    This helper is intentionally non-destructive: existing files are preserved.
    """
    for directory in (UNIT_RESULTS_DIR, ARTICLE_RESULTS_DIR, PLOTS_DIR, ARTICLE_IMAGES_DIR):
        directory.mkdir(parents=True, exist_ok=True)

    return {
        "unit_results_dir": UNIT_RESULTS_DIR,
        "article_results_dir": ARTICLE_RESULTS_DIR,
        "plots_dir": PLOTS_DIR,
        "article_images_dir": ARTICLE_IMAGES_DIR,
    }
