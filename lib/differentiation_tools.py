"""
lib/differentiation_tools.py
-----------------------------
Numerical differentiation methods for ECE 5110.

Contains only the numerical computation class.
Plotting utilities belong in the test/demo scripts.
"""


class DifferentiationTools:
    """
    Numerical differentiation utilities using 3-point finite-difference formulas.

    Methods
    -------
    numerical_differentiation_3point(f, x, h, method)
        Approximate the first derivative of f at x using a 3-point formula.
    """

    def numerical_differentiation_3point(self, f, x, h=1e-5, method="central"):
        """
        Approximate f'(x) using a 3-point finite-difference formula.

        Parameters
        ----------
        f : callable
            The function to differentiate.
        x : float
            The point at which to evaluate the derivative.
        h : float, optional
            Step size (must be > 0). Default is 1e-5.
        method : str, optional
            One of ``"central"``, ``"forward"``, or ``"backward"``.
            Default is ``"central"``.

        Returns
        -------
        float
            Approximation of f'(x).

        Raises
        ------
        ValueError
            If ``h <= 0`` or ``method`` is not a recognised option.

        Notes
        -----
        Formulas (all second-order accurate):

        Central:
            f'(x) ≈ [f(x+h) − f(x−h)] / (2h)

        Forward:
            f'(x) ≈ [−3f(x) + 4f(x+h) − f(x+2h)] / (2h)

        Backward:
            f'(x) ≈ [f(x−2h) − 4f(x−h) + 3f(x)] / (2h)
        """
        if h <= 0:
            raise ValueError(f"h must be positive, got h={h!r}")

        if method == "central":
            return (f(x + h) - f(x - h)) / (2 * h)
        elif method == "forward":
            return (-3 * f(x) + 4 * f(x + h) - f(x + 2 * h)) / (2 * h)
        elif method == "backward":
            return (f(x - 2 * h) - 4 * f(x - h) + 3 * f(x)) / (2 * h)
        else:
            raise ValueError(
                f"method must be 'central', 'forward', or 'backward', got {method!r}"
            )
