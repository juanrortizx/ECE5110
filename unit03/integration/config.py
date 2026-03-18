"""Configuration and benchmarks for Unit 03 integration workflow."""

import math
import numpy as np

N_VALUES = [4, 8, 16, 32, 64, 128, 256]
EXPECTED_ORDER_TRAPEZOIDAL = 2.0
EXPECTED_ORDER_SIMPSON = 4.0
MIN_ORDER_TRAPEZOIDAL = 1.8
MIN_ORDER_SIMPSON = 3.7

BENCHMARK_CASES = [
    {
        "name": "x_squared",
        "display_name": "Integral of x^2 on [0,1]",
        "f": lambda x: x**2,
        "a": 0.0,
        "b": 1.0,
        "exact": 1.0 / 3.0,
    },
    {
        "name": "sine",
        "display_name": "Integral of sin(x) on [0,pi]",
        "f": np.sin,
        "a": 0.0,
        "b": float(np.pi),
        "exact": 2.0,
    },
    {
        "name": "exp",
        "display_name": "Integral of exp(x) on [0,1]",
        "f": np.exp,
        "a": 0.0,
        "b": 1.0,
        "exact": float(math.e - 1.0),
    },
    {
        "name": "pi_integrand",
        "display_name": "Integral of 4/(1+x^2) on [0,1]",
        "f": lambda x: 4.0 / (1.0 + x**2),
        "a": 0.0,
        "b": 1.0,
        "exact": float(np.pi),
    },
]
