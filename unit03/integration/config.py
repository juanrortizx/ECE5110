"""Configuration and benchmark definitions for Unit 03 integration workflows."""

from pathlib import Path

import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
UNIT03_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = UNIT03_DIR.parent

UNIT_RESULTS_DIR = UNIT03_DIR / "results"
ARTICLE_RESULTS_DIR = UNIT_RESULTS_DIR / "article_results"
PLOTS_DIR = UNIT_RESULTS_DIR / "plots"
ARTICLE_IMAGES_DIR = UNIT_RESULTS_DIR / "article_images"

N_VALUES = [4, 8, 16, 32, 64, 128, 256]
EXPECTED_ORDERS = {"trapezoidal": 2.0, "simpson": 4.0}
MIN_OBSERVED_ORDERS = {"trapezoidal": 1.8, "simpson": 3.5}

BENCHMARK_CASES = [
    {
        "name": "poly_x_squared",
        "display_name": r"Integral of x^2 on [0, 1]",
        "f": lambda x: x**2,
        "a": 0.0,
        "b": 1.0,
        "exact": 1.0 / 3.0,
        "trapezoidal_tol": 1.0e-5,
        "simpson_tol": 1.0e-9,
    },
    {
        "name": "sin_x",
        "display_name": r"Integral of sin(x) on [0, pi]",
        "f": np.sin,
        "a": 0.0,
        "b": float(np.pi),
        "exact": 2.0,
        "trapezoidal_tol": 3.0e-5,
        "simpson_tol": 1.0e-9,
    },
    {
        "name": "exp_x",
        "display_name": r"Integral of exp(x) on [0, 1]",
        "f": np.exp,
        "a": 0.0,
        "b": 1.0,
        "exact": float(np.e - 1.0),
        "trapezoidal_tol": 1.0e-5,
        "simpson_tol": 1.0e-9,
    },
    {
        "name": "four_over_one_plus_x2",
        "display_name": r"Integral of 4/(1+x^2) on [0, 1]",
        "f": lambda x: 4.0 / (1.0 + x**2),
        "a": 0.0,
        "b": 1.0,
        "exact": float(np.pi),
        "trapezoidal_tol": 1.0e-5,
        "simpson_tol": 1.0e-9,
    },
]
