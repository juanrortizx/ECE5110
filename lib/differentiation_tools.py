"""Numerical differentiation kernels for Unit 03 workflows.

This module intentionally keeps only core numerical methods. Plotting and
reporting logic belong in Unit 03 workflow helpers.
"""


class DifferentiationTools:
    """Container for finite-difference differentiation methods."""

    def numerical_differentiation_3point(self, f, x, h=1e-5, method="central"):
        """Approximate first derivative using a 3-point finite-difference stencil.

        Parameters
        ----------
        f : callable
            Function to differentiate.
        x : float
            Evaluation point.
        h : float, default=1e-5
            Step size. Must be positive.
        method : {"central", "forward", "backward"}, default="central"
            Stencil selection.
        """
        if h <= 0:
            raise ValueError("h must be positive")

        if method == "central":
            return (f(x + h) - f(x - h)) / (2.0 * h)
        if method == "forward":
            return (-3.0 * f(x) + 4.0 * f(x + h) - f(x + 2.0 * h)) / (2.0 * h)
        if method == "backward":
            return (f(x - 2.0 * h) - 4.0 * f(x - h) + 3.0 * f(x)) / (2.0 * h)

        raise ValueError("method must be 'central', 'forward', or 'backward'")
