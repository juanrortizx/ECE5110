"""Numerical integration kernels for Unit 03 workflows.

This module only contains integration formulas and validation logic.
Plot generation and artifact exports are handled by Unit 03 helper modules.
"""

import numpy as np


class IntegrationTools:
    """Collection of composite numerical integration methods."""

    def composite_trapezoidal(self, f, a, b, n):
        """Approximate an integral using the composite trapezoidal rule.

        Parameters
        ----------
        f : callable
            Integrand accepting scalar or NumPy array input.
        a : float
            Lower integration bound.
        b : float
            Upper integration bound.
        n : int
            Number of subintervals.

        Returns
        -------
        float
            Numerical integral approximation.

        Raises
        ------
        TypeError
            If ``f`` is not callable.
        ValueError
            If ``n <= 0`` or ``a == b``.
        """
        if not callable(f):
            raise TypeError("f must be callable.")
        if n <= 0:
            raise ValueError("n must be positive.")
        if a == b:
            raise ValueError("a and b must define a non-zero interval.")

        h = (b - a) / float(n)
        x = np.linspace(a, b, n + 1)
        y = f(x)
        return float(h * (0.5 * y[0] + np.sum(y[1:-1]) + 0.5 * y[-1]))

    def composite_simpson(self, f, a, b, n):
        """Approximate an integral using composite Simpson's rule.

        Parameters
        ----------
        f : callable
            Integrand accepting scalar or NumPy array input.
        a : float
            Lower integration bound.
        b : float
            Upper integration bound.
        n : int
            Number of subintervals (must be even).

        Returns
        -------
        float
            Numerical integral approximation.

        Raises
        ------
        TypeError
            If ``f`` is not callable.
        ValueError
            If ``n <= 0``, ``n`` is odd, or ``a == b``.
        """
        if not callable(f):
            raise TypeError("f must be callable.")
        if n <= 0:
            raise ValueError("n must be positive.")
        if n % 2 != 0:
            raise ValueError("n must be even for composite Simpson's rule.")
        if a == b:
            raise ValueError("a and b must define a non-zero interval.")

        h = (b - a) / float(n)
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
