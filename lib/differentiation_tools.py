"""Numerical differentiation kernels for Unit 03 workflows.

This module intentionally contains only numerical-method kernels. Plotting,
artifact generation, and reporting are handled by workflow helper packages.
"""

from __future__ import annotations


class DifferentiationTools:
    """Finite-difference numerical differentiation utilities.

    Notes
    -----
    Only numerical differentiation methods belong in this class. Plotting and
    report-generation logic should remain in workflow helper modules.
    """

    def numerical_differentiation_3point(self, f, x, h=1e-5, method="central"):
        """Approximate the first derivative using 3-point finite differences.

        Parameters
        ----------
        f : callable
            Scalar function to differentiate.
        x : float
            Evaluation point.
        h : float, optional
            Positive step size.
        method : {"central", "forward", "backward"}, optional
            3-point stencil to use.

        Returns
        -------
        float
            First derivative approximation at ``x``.

        Raises
        ------
        ValueError
            If ``h <= 0`` or ``method`` is unsupported.
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
