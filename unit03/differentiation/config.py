"""Configuration and benchmark definitions for Unit 03 differentiation."""

import numpy as np

METHODS = ("central", "forward", "backward")
H_VALUES = np.logspace(-1, -8, 80)


TEST_CASES = [
    {
        "name": "sine_at_pi_over_4",
        "display_name": "sin(x) at x=pi/4",
        "f": np.sin,
        "df": np.cos,
        "x": float(np.pi / 4.0),
        "h": 1e-5,
        "tolerances": {"central": 1e-8, "forward": 1e-6, "backward": 1e-6},
    },
    {
        "name": "exp_at_0p3",
        "display_name": "exp(x) at x=0.3",
        "f": np.exp,
        "df": np.exp,
        "x": 0.3,
        "h": 1e-5,
        "tolerances": {"central": 1e-8, "forward": 2e-6, "backward": 2e-6},
    },
    {
        "name": "poly_cubic_minus_quadratic",
        "display_name": "x^3 - 2x^2 + x - 5 at x=1.2",
        "f": lambda x: x**3 - 2.0 * x**2 + x - 5.0,
        "df": lambda x: 3.0 * x**2 - 4.0 * x + 1.0,
        "x": 1.2,
        "h": 1e-5,
        "tolerances": {"central": 1e-7, "forward": 1e-5, "backward": 1e-5},
    },
]

FREEFALL_POSITION_DATA = np.array([0.0, -0.05, -0.10, -0.15, -0.20, -0.25, -0.30], dtype=float)
FREEFALL_TIME_DATA = np.array([0.0, 0.100764, 0.141736, 0.174306, 0.201042, 0.224583, 0.247569], dtype=float)
FREEFALL_GRAVITY_TOL = 0.15
