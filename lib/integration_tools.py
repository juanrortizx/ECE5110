"""Numerical integration kernels for Unit 03 workflows.

This module intentionally contains only reusable numerical kernels. Plotting,
artifact export, and workflow orchestration live in unit03 helpers.
"""

import numpy as np


class IntegrationTools:
    """Container for composite numerical integration methods."""

    def composite_trapezoidal(self, f, a, b, n):
        """Approximate the definite integral using composite trapezoidal rule."""
        if not callable(f):
            raise TypeError("f must be callable")
        if n <= 0:
            raise ValueError("n must be positive")
        if a == b:
            raise ValueError("a and b must define a nonzero interval")

        h = (b - a) / float(n)
        x = np.linspace(a, b, n + 1, dtype=float)
        y = np.asarray(f(x), dtype=float)
        return h * (0.5 * y[0] + np.sum(y[1:-1]) + 0.5 * y[-1])

    def composite_simpson(self, f, a, b, n):
        """Approximate the definite integral using composite Simpson's rule."""
        if not callable(f):
            raise TypeError("f must be callable")
        if n <= 0:
            raise ValueError("n must be positive")
        if n % 2 != 0:
            raise ValueError("n must be even for Simpson's rule")
        if a == b:
            raise ValueError("a and b must define a nonzero interval")

        h = (b - a) / float(n)
        x = np.linspace(a, b, n + 1, dtype=float)
        y = np.asarray(f(x), dtype=float)
        return (h / 3.0) * (
            y[0]
            + y[-1]
            + 4.0 * np.sum(y[1:-1:2])
            + 2.0 * np.sum(y[2:-1:2])
        )
