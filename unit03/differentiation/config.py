"""Configuration constants for the Unit 03 differentiation workflow."""

from pathlib import Path

import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
UNIT_RESULTS_DIR = PROJECT_ROOT / "unit03" / "results"
ARTICLE_RESULTS_DIR = UNIT_RESULTS_DIR / "article_results"
PLOTS_DIR = UNIT_RESULTS_DIR / "plots"
ARTICLE_IMAGES_DIR = UNIT_RESULTS_DIR / "article_images"

TEST_CASES = (
    {
        "name": "sine_at_pi_over_4",
        "display_name": "sin(x) at x = pi/4",
        "f": np.sin,
        "df": np.cos,
        "x": float(np.pi / 4.0),
        "h": 1e-5,
        "tolerances": {"central": 1e-8, "forward": 1e-7, "backward": 1e-7},
    },
    {
        "name": "exp_at_0p3",
        "display_name": "exp(x) at x = 0.3",
        "f": np.exp,
        "df": np.exp,
        "x": 0.3,
        "h": 1e-5,
        "tolerances": {"central": 1e-8, "forward": 1e-7, "backward": 1e-7},
    },
    {
        "name": "poly_cubic_minus_quadratic",
        "display_name": "x^3 - 2x^2 + x - 5 at x = 1.2",
        "f": lambda x: x**3 - 2.0 * x**2 + x - 5.0,
        "df": lambda x: 3.0 * x**2 - 4.0 * x + 1.0,
        "x": 1.2,
        "h": 1e-5,
        "tolerances": {"central": 1e-8, "forward": 1e-7, "backward": 1e-7},
    },
)

METHODS = ("central", "forward", "backward")
H_VALUES = np.logspace(-1, -8, 80)

FREEFALL_POSITION_DATA = np.array(
    [0.0, -0.05, -0.10, -0.15, -0.20, -0.25, -0.30],
    dtype=float,
)
FREEFALL_TIME_DATA = np.array(
    [0.0, 0.100764, 0.141736, 0.174306, 0.201042, 0.224583, 0.247569],
    dtype=float,
)
FREEFALL_GRAVITY_TOL = 0.15

__all__ = [
    "SCRIPT_DIR",
    "PROJECT_ROOT",
    "UNIT_RESULTS_DIR",
    "ARTICLE_RESULTS_DIR",
    "PLOTS_DIR",
    "ARTICLE_IMAGES_DIR",
    "TEST_CASES",
    "METHODS",
    "H_VALUES",
    "FREEFALL_POSITION_DATA",
    "FREEFALL_TIME_DATA",
    "FREEFALL_GRAVITY_TOL",
]
