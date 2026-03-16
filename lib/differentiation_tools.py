"""Numerical differentiation utilities for Unit 03.

This module intentionally focuses on finite-difference derivative approximations.
Plotting and report-generation utilities belong in test/demo scripts.
"""


class DifferentiationTools:
    """Provide 3-point finite-difference derivative approximations.

    Notes
    -----
    This class contains only numerical differentiation methods. Plotting logic is
    intentionally excluded and should be implemented in the calling script.
    """

    def numerical_differentiation_3point(self, f, x, h=1e-5, method="central"):
        """Approximate the first derivative with a 3-point finite difference.

        Parameters
        ----------
        f : callable
            Function to differentiate.
        x : float
            Evaluation point.
        h : float, optional
            Step size. Must be strictly positive.
        method : {"central", "forward", "backward"}, optional
            Finite-difference stencil.

        Returns
        -------
        float
            Approximation to f'(x).

        Raises
        ------
        ValueError
            If ``h <= 0`` or ``method`` is not supported.
        """
        if h <= 0:
            raise ValueError("h must be strictly positive")

        if method == "central":
            return (f(x + h) - f(x - h)) / (2.0 * h)
        if method == "forward":
            return (-3.0 * f(x) + 4.0 * f(x + h) - f(x + 2.0 * h)) / (2.0 * h)
        if method == "backward":
            return (f(x - 2.0 * h) - 4.0 * f(x - h) + 3.0 * f(x)) / (2.0 * h)

        raise ValueError("method must be 'central', 'forward', or 'backward'")
