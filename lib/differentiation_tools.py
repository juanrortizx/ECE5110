"""Numerical differentiation kernels for Unit 03 workflows.

This module intentionally contains only differentiation formulas and validation.
Plotting and reporting utilities belong to the Unit 03 helper/test workflows.
"""


class DifferentiationTools:
    """Collection of finite-difference differentiation methods."""

    def numerical_differentiation_3point(self, f, x, h=1e-5, method="central"):
        """Approximate a first derivative with a 3-point finite-difference scheme.

        Parameters
        ----------
        f : callable
            Function to differentiate.
        x : float
            Evaluation location.
        h : float, optional
            Step size, by default 1e-5.
        method : {"central", "forward", "backward"}, optional
            Finite-difference formula to use.

        Returns
        -------
        float
            Numerical derivative approximation.

        Raises
        ------
        ValueError
            If ``h <= 0`` or if ``method`` is unsupported.
        """
        if h <= 0:
            raise ValueError("h must be positive.")

        if method == "central":
            return (f(x + h) - f(x - h)) / (2.0 * h)
        if method == "forward":
            return (-3.0 * f(x) + 4.0 * f(x + h) - f(x + 2.0 * h)) / (2.0 * h)
        if method == "backward":
            return (f(x - 2.0 * h) - 4.0 * f(x - h) + 3.0 * f(x)) / (2.0 * h)

        raise ValueError("method must be one of: 'central', 'forward', 'backward'.")
