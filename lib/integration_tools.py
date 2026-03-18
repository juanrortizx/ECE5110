"""Numerical integration kernels for Unit 03 workflows.

This module only contains integration kernels. Plotting, artifacts, and report
logic belong in helper workflows under ``unit03/integration``.
"""

from __future__ import annotations

import numpy as np


class IntegrationTools:
    """Composite numerical integration methods."""

    def composite_trapezoidal(self, f, a, b, n):
        """Approximate an integral with the composite trapezoidal rule.

        Parameters
        ----------
        f : callable
            Integrand that accepts NumPy arrays.
        a, b : float
            Integration bounds.
        n : int
            Number of uniform subintervals (must be positive).

        Returns
        -------
        float
            Approximation of the definite integral.
        """
        if not callable(f):
            raise TypeError("f must be callable.")
        if n <= 0:
            raise ValueError("n must be positive.")
        if a == b:
            raise ValueError("a and b must define a nonzero interval.")

        h = (b - a) / float(n)
        x = np.linspace(a, b, n + 1)
        y = f(x)
        return float(h * (0.5 * y[0] + np.sum(y[1:-1]) + 0.5 * y[-1]))

    def composite_simpson(self, f, a, b, n):
        """Approximate an integral with composite Simpson's rule.

        Parameters
        ----------
        f : callable
            Integrand that accepts NumPy arrays.
        a, b : float
            Integration bounds.
        n : int
            Number of uniform subintervals (must be positive and even).

        Returns
        -------
        float
            Approximation of the definite integral.
        """
        if not callable(f):
            raise TypeError("f must be callable.")
        if n <= 0:
            raise ValueError("n must be positive.")
        if n % 2 != 0:
            raise ValueError("n must be even for Simpson's rule.")
        if a == b:
            raise ValueError("a and b must define a nonzero interval.")

        h = (b - a) / float(n)
        x = np.linspace(a, b, n + 1)
        y = f(x)
        return float(
            (h / 3.0)
            * (y[0] + y[-1] + 4.0 * np.sum(y[1:-1:2]) + 2.0 * np.sum(y[2:-1:2]))
        )
