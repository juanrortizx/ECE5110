"""Configuration for Unit 03 integration workflows."""

from __future__ import annotations

import numpy as np

from unit03.common.paths import (
    ARTICLE_IMAGES_DIR,
    ARTICLE_RESULTS_DIR,
    PLOTS_DIR,
    PROJECT_ROOT,
    UNIT_RESULTS_DIR,
)


SCRIPT_DIR = PROJECT_ROOT / "unit03" / "test"
N_VALUES = [4, 8, 16, 32, 64, 128, 256]
METHODS = ("trapezoidal", "simpson")
METHOD_TOOL_MAP = {
    "trapezoidal": "composite_trapezoidal",
    "simpson": "composite_simpson",
}
EXPECTED_ORDER = {"trapezoidal": 2.0, "simpson": 4.0}
MIN_OBSERVED_ORDER = {"trapezoidal": 1.8, "simpson": 3.6}

BENCHMARK_CASES = (
    {
        "name": "x_squared",
        "display_name": "Integral of x^2 on [0,1]",
        "f": lambda x: x**2,
        "a": 0.0,
        "b": 1.0,
        "exact": 1.0 / 3.0,
    },
    {
        "name": "sin_on_pi",
        "display_name": "Integral of sin(x) on [0,pi]",
        "f": np.sin,
        "a": 0.0,
        "b": float(np.pi),
        "exact": 2.0,
    },
    {
        "name": "exp_on_01",
        "display_name": "Integral of exp(x) on [0,1]",
        "f": np.exp,
        "a": 0.0,
        "b": 1.0,
        "exact": float(np.e - 1.0),
    },
    {
        "name": "pi_form",
        "display_name": "Integral of 4/(1+x^2) on [0,1]",
        "f": lambda x: 4.0 / (1.0 + x**2),
        "a": 0.0,
        "b": 1.0,
        "exact": float(np.pi),
    },
)
