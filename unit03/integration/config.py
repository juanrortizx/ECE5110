"""Configuration constants for Unit 03 integration workflows."""

from pathlib import Path

import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
UNIT_RESULTS_DIR = PROJECT_ROOT / "unit03" / "results"
ARTICLE_RESULTS_DIR = UNIT_RESULTS_DIR / "article_results"
PLOTS_DIR = UNIT_RESULTS_DIR / "plots"
ARTICLE_IMAGES_DIR = UNIT_RESULTS_DIR / "article_images"

N_VALUES = [4, 8, 16, 32, 64, 128, 256]
TRAPEZOIDAL_ORDER_TARGET = 2.0
SIMPSON_ORDER_TARGET = 4.0

BENCHMARK_CASES = (
    {
        "case_name": "poly_x_squared",
        "display_name": "Integral of x^2 on [0, 1]",
        "f": lambda x: x**2,
        "a": 0.0,
        "b": 1.0,
        "exact": 1.0 / 3.0,
        "trap_tol": 3.0e-6,
        "simp_tol": 1.0e-12,
    },
    {
        "case_name": "sin_0_to_pi",
        "display_name": "Integral of sin(x) on [0, pi]",
        "f": np.sin,
        "a": 0.0,
        "b": float(np.pi),
        "exact": 2.0,
        "trap_tol": 3.0e-5,
        "simp_tol": 5.0e-10,
    },
    {
        "case_name": "exp_0_to_1",
        "display_name": "Integral of exp(x) on [0, 1]",
        "f": np.exp,
        "a": 0.0,
        "b": 1.0,
        "exact": float(np.e - 1.0),
        "trap_tol": 3.0e-6,
        "simp_tol": 1.0e-11,
    },
    {
        "case_name": "pi_integral",
        "display_name": "Integral of 4/(1+x^2) on [0, 1]",
        "f": lambda x: 4.0 / (1.0 + x**2),
        "a": 0.0,
        "b": 1.0,
        "exact": float(np.pi),
        "trap_tol": 5.0e-6,
        "simp_tol": 1.0e-11,
    },
)

__all__ = [
    "SCRIPT_DIR",
    "PROJECT_ROOT",
    "UNIT_RESULTS_DIR",
    "ARTICLE_RESULTS_DIR",
    "PLOTS_DIR",
    "ARTICLE_IMAGES_DIR",
    "N_VALUES",
    "TRAPEZOIDAL_ORDER_TARGET",
    "SIMPSON_ORDER_TARGET",
    "BENCHMARK_CASES",
]
