"""Numerical integration utilities for Unit 03.

This module intentionally focuses on reusable quadrature routines.
Plotting and report-generation utilities belong in test/demo scripts.
"""

import numpy as np


class IntegrationTools:
    """Provide composite numerical integration methods."""

    def composite_trapezoidal(self, f, a, b, n):
        """Approximate an integral with the composite trapezoidal rule.

        Parameters
        ----------
        f : callable
            Integrand that supports NumPy-array input.
        a : float
            Lower integration bound.
        b : float
            Upper integration bound.
        n : int
            Number of subintervals. Must be strictly positive.

        Returns
        -------
        float
            Approximation to the definite integral.

        Raises
        ------
        TypeError
            If ``f`` is not callable.
        ValueError
            If ``n <= 0`` or ``a == b``.
        """
        if not callable(f):
            raise TypeError("f must be callable")
        if n <= 0:
            raise ValueError("n must be strictly positive")
        if a == b:
            raise ValueError("integration interval must have nonzero width")

        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        y = f(x)
        return float(h * (0.5 * y[0] + np.sum(y[1:-1]) + 0.5 * y[-1]))

    def composite_simpson(self, f, a, b, n):
        """Approximate an integral with the composite Simpson rule.

        Parameters
        ----------
        f : callable
            Integrand that supports NumPy-array input.
        a : float
            Lower integration bound.
        b : float
            Upper integration bound.
        n : int
            Number of subintervals. Must be strictly positive and even.

        Returns
        -------
        float
            Approximation to the definite integral.

        Raises
        ------
        TypeError
            If ``f`` is not callable.
        ValueError
            If ``n <= 0``, ``n`` is odd, or ``a == b``.
        """
        if not callable(f):
            raise TypeError("f must be callable")
        if n <= 0:
            raise ValueError("n must be strictly positive")
        if n % 2 != 0:
            raise ValueError("n must be even for composite Simpson's rule")
        if a == b:
            raise ValueError("integration interval must have nonzero width")

        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        y = f(x)
        return float(
            (h / 3.0)
            * (
                y[0]
                + y[-1]
                + 4.0 * np.sum(y[1:-1:2])
                + 2.0 * np.sum(y[2:-1:2])
            )
        )