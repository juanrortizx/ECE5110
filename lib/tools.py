import numpy as np

class Tools:

#---------------------------------------------------------------------------------------
# Unit 01: Solutions of Equations in One Variable
#---------------------------------------------------------------------------------------
    def solve_bisection_rec(self, f, a, b, precision, max_steps):
        if max_steps <= 0:
            return 0, -2
        if a > b:
            return 0, -1
        if f(a) * f(b) > 0:
            return 0, -1
        
        if abs(f(a)) < precision:
            return a, 0
        if abs(f(b)) < precision:
            return b, 0 
        
        mid = (a + b) / 2  
        if f(a) * f(mid) > 0:
            return self.solve_bisection_rec(f, mid, b, precision, max_steps - 1)
        
        return self.solve_bisection_rec(f, a, mid, precision, max_steps - 1)
    
    def solve_bisection_loop(self, f, a, b, precision = 1e-6, max_steps = 100):
        if abs(f(a)) < precision:
            return a, 0
        if abs(f(b)) < precision:
            return b, 0
        if f(a) * f(b) > 0:
            return 0, -1
        
        for _ in range(max_steps):
            c = (a + b) / 2
            if abs(f(c)) < precision or (b - a) / 2 < precision:
                return c, 0
            if f(a) * f(c) < 0:
                b = c
            else:
                a = c
        return c, -2
    
    def solve_fixed_point(self, f, x0, tolerance=1e-8, max_steps=100):
        x = x0

        for i in range(1, max_steps + 1):
            fx = f(x)
            residual = abs(x - fx)

            if residual < tolerance:
                return fx, i, 0   # success

            x = fx

        return x, max_steps, -2  # failure
    
    def solve_newton_method(self, f, df, x0, tolerance=1e-8, max_steps=100):
        x = x0

        for i in range(1, max_steps + 1):
            dfx = df(x)
            if dfx == 0:
                return x, i, -1

            fx = f(x)
            x_new = x - fx / dfx

            if abs(x_new - x) < tolerance:
                return x_new, i, 0

            x = x_new

        return x, max_steps, -2
    
#---------------------------------------------------------------------------------------
# Unit 02: Interpolation and Polynomial Approximation 
#---------------------------------------------------------------------------------------
    def _divided_differences(self, x, y):
        """
        Internal helper to compute the Newton divided differences.
        Returns the coefficient vector a where:
          a[0] = f[x0],
          a[1] = f[x0,x1],
          ...
          a[n-1] = f[x0,...,xn-1]
        """
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)

        if x.ndim != 1 or y.ndim != 1 or x.size != y.size:
            raise ValueError("x and y must be 1-D arrays of the same length.")
        if np.unique(x).size != x.size:
            raise ValueError("All x-values must be distinct for interpolation.")

        n = x.size
        # Copy y into a working column; this will be overwritten into divided differences
        coef = y.astype(float).copy()

        # Build the upper triangular table in-place in coef
        for j in range(1, n):
            # coef[i] becomes f[x_i, ..., x_{i+j}]
            coef[j:n] = (coef[j:n] - coef[j-1:n-1]) / (x[j:n] - x[0:n-j])

        return coef  # length n

    def newton_interpolator(self, x, y):
        """
        Build the Newton-form interpolating polynomial using divided differences.
        Returns:
          N   : callable evaluator (scalar or vector X)
          a   : numpy array of Newton coefficients [a0, a1, ..., a_{n-1}]
          x   : numpy array of nodes (returned for convenience)
        """
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)
        a = self._divided_differences(x, y)
        n = len(a)

        def N(X):
            """
            Horner-like evaluation in Newton form:
              P(x) = a0 + (x-x0)[a1 + (x-x1)[a2 + ... ]]
            Works for scalar or vector X.
            """
            X = np.asarray(X, dtype=float)
            # Start from the highest coefficient a_{n-1}
            p = np.full_like(X, fill_value=a[-1], dtype=float)
            for k in range(n-2, -1, -1):
                p = a[k] + (X - x[k]) * p
            return p

        return N, a, x

    def newton_poly1d(self, x, y):
        """
        Expand the Newton polynomial to a standard numpy.poly1d (optional utility).
        Useful for printing coefficients, derivatives, roots, etc.
        """
        from numpy.polynomial.polynomial import Polynomial  # safe, no internet needed

        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)
        a = self._divided_differences(x, y)
        n = len(a)

        # Build polynomial in increasing-power form using numpy.polynomial
        P = Polynomial([0.0])
        basis = Polynomial([1.0])  # starts as 1

        for k in range(n):
            P = P + a[k] * basis
            # Update basis *= (x - x_k)
            basis = basis * Polynomial([-x[k], 1.0])

        # Convert to poly1d (descending powers) for familiarity if desired
        return np.poly1d(P.convert().coef[::-1])

    def lagrange_interpolator(self, x, y):
        """
        Build the Lagrange interpolation polynomial P based on points (x, y).
        Returns a callable P(X) that accepts scalar or numpy array X.
        Requirements:
          - x and y must be 1-D arrays of same length
          - all x's must be distinct
        """
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)

        if x.ndim != 1 or y.ndim != 1 or x.size != y.size:
            raise ValueError("x and y must be 1-D arrays of the same length.")
        if np.unique(x).size != x.size:
            raise ValueError("All x-values must be distinct for Lagrange interpolation.")

        n = x.size

        # Precompute denominators: d_k = ∏_{i≠k} (x_k - x_i)
        denom = np.empty(n, dtype=float)
        for k in range(n):
            diff = x[k] - np.delete(x, k)
            denom[k] = np.prod(diff)
            if denom[k] == 0.0:
                raise ZeroDivisionError("Duplicate x-values detected.")

        def P(X):
            # Vectorized evaluation: X can be scalar or array
            X = np.asarray(X, dtype=float)
            out = np.zeros_like(X, dtype=float)

            # Direct Lagrange assembly: P(X) = Σ y_k * L_k(X)
            # with L_k(X) = ∏_{i≠k} (X - x_i) / (x_k - x_i)
            for k in range(n):
                num = np.ones_like(X, dtype=float)
                for i in range(n):
                    if i == k:
                        continue
                    num *= (X - x[i])
                out += y[k] * (num / denom[k])

            return out

        return P

#---------------------------------------------------------------------------------------
# Unit 03: Numerical Integration and Differentiation
#---------------------------------------------------------------------------------------

    def midpoint_rule(self, f, a, b, n):
        if n <= 0:
            raise ValueError("Number of subintervals n must be positive.")
        
        a = float(a); b = float(b)
        h = (b - a) / n # width of each subinterval
        midpoints = a + h * (np.arange(n) + 0.5) # midpoints of subintervals

        return h * np.sum(f(midpoints)) # sum of f at midpoints times width
    
    def trapezoidal_rule(self, f, a, b, n):
        if n <= 0:
            raise ValueError("Number of subintervals n must be positive.")
        
        a = float(a); b = float(b)
        h = (b - a) / n # width of each subinterval
        x = a + h * np.arange(n + 1) # endpoints of subintervals

        return (h / 2) * (f(x[0]) + 2 * np.sum(f(x[1:n])) + f(x[n])) # trapezoidal sum

    def simpsons_rule(self, f, a, b, n):
        if n <= 0 or n % 2 != 0:
            raise ValueError("Number of subintervals n must be a positive even integer.")
        
        a = float(a); b = float(b)
        h = (b - a) / n # width of each subinterval
        x = a + h * np.arange(n + 1) # endpoints of subintervals

        return (h / 3) * (f(x[0]) + 
                          4 * np.sum(f(x[1:n:2])) + 
                          2 * np.sum(f(x[2:n-1:2])) + 
                          f(x[n])) # Simpson's sum

#---------------------------------------------------------------------------------------
# Unit 03.5: Differentiation and Integration AI Group Project
#---------------------------------------------------------------------------------------

    def composite_trapezoidal(self, f, a, b, n):
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

    def numerical_differentiation_3point(self, f, x, h=1e-5, method='central'):
        if h <= 0:
            raise ValueError("h must be strictly positive")

        if method == 'central':
            return (f(x + h) - f(x - h)) / (2 * h)
        elif method == 'forward':
            return (-3 * f(x) + 4 * f(x + h) - f(x + 2 * h)) / (2 * h)
        elif method == 'backward':
            return (f(x - 2 * h) - 4 * f(x - h) + 3 * f(x)) / (2 * h)
        else:
            raise ValueError("method must be 'central', 'forward', or 'backward'")

#---------------------------------------------------------------------------------------
# Unit 04: Solving Linear Systems
#---------------------------------------------------------------------------------------

## Linear Systems of Equations (LSoE) and Cubic Splines

    def solve_lsoe(self, A, B):
        err = 0
        A = np.array(A, dtype=float, copy=True)
        B = np.array(B, dtype=float, copy=True).reshape(-1)
        n = A.shape[0]
        sol = np.zeros(n, dtype=float)

        if A.ndim != 2 or A.shape[1] != n or B.shape[0] != n:
            raise ValueError(
                f"Matrix dimensions must agree: A is {A.shape[0]}x{A.shape[1]}, B is {B.shape[0]}x1"
            )

        # Forward elimination with partial pivoting
        for ix in range(n - 1):
            pivotRow = ix + np.argmax(np.abs(A[ix:n, ix]))
            pivotVal = A[pivotRow, ix]

            if np.isclose(pivotVal, 0.0):
                err = 1
                raise ValueError("Matrix is singular or nearly singular.")

            if pivotRow != ix:
                A[[ix, pivotRow], :] = A[[pivotRow, ix], :]
                B[[ix, pivotRow]] = B[[pivotRow, ix]]

            for row in range(ix + 1, n):
                factor = A[row, ix] / A[ix, ix]
                A[row, ix:n] = A[row, ix:n] - factor * A[ix, ix:n]
                B[row] = B[row] - factor * B[ix]

        # Back substitution
        for ix in range(n - 1, -1, -1):
            if np.isclose(A[ix, ix], 0.0):
                err = 1
                raise ValueError("Matrix is singular or nearly singular.")
            sol[ix] = (B[ix] - np.dot(A[ix, ix + 1:n], sol[ix + 1:n])) / A[ix, ix]

        return sol, err

    def cubic_splines(self, X, Y, return_details=False):
        X = np.asarray(X, dtype=float)
        Y = np.asarray(Y, dtype=float)
        err = 0
        n = len(X)
        
        if n != len(Y):
            err = 1
            raise ValueError(f"Matrix dimensions must agree: X is {n}x1, Y is {len(Y)}x1")
        
        if n < 2:
            err = 1
            raise ValueError("At least two data points are required.")
        
        # Number of spline segments
        m = n - 1
        
        # Each segment has 4 coefficients: a_i, b_i, c_i, d_i
        # Total unknowns = 4 * (n - 1)
        A = np.zeros((4 * m, 4 * m))
        B = np.zeros(4 * m)
        row = 0
        
        # 1) Each spline passes through its left endpoint
        for i in range(m):
            col = 4 * i
            A[row, col:col+4] = [X[i]**3, X[i]**2, X[i], 1]
            B[row] = Y[i]
            row += 1
        
        # 2) Each spline passes through its right endpoint
        for i in range(m):
            col = 4 * i
            A[row, col:col+4] = [X[i + 1]**3, X[i + 1]**2, X[i + 1], 1]
            B[row] = Y[i + 1]
            row += 1
        
        # 3) First derivative continuity at interior knots
        for i in range(m - 1):
            xk = X[i + 1]
            col1 = 4 * i
            col2 = 4 * (i + 1)
            A[row, col1:col1+3] = [3 * xk**2, 2 * xk, 1]
            A[row, col2:col2+3] = [-3 * xk**2, -2 * xk, -1]
            B[row] = 0
            row += 1
        
        # 4) Second derivative continuity at interior knots
        for i in range(m - 1):
            xk = X[i + 1]
            col1 = 4 * i
            col2 = 4 * (i + 1)
            A[row, col1:col1+2] = [6 * xk, 2]
            A[row, col2:col2+2] = [-6 * xk, -2]
            B[row] = 0
            row += 1
        
        # 5) Natural spline boundary conditions
        # S_1''(X_1) = 0
        A[row, :4] = [6 * X[0], 2, 0, 0]
        B[row] = 0
        row += 1
        
        # S_m''(X_n) = 0
        lastCol = 4 * (m - 1)
        A[row, lastCol:lastCol+2] = [6 * X[n-1], 2]
        B[row] = 0
        row += 1
        
        # Solve the linear system
        sol, err = self.solve_lsoe(A, B)

        def S(Xq):
            """Evaluate the natural cubic spline at scalar or vector query points."""
            Xq = np.asarray(Xq, dtype=float)
            Yq = np.empty_like(Xq, dtype=float)

            for idx, xv in np.ndenumerate(Xq):
                seg = np.searchsorted(X, xv, side="right") - 1
                seg = int(np.clip(seg, 0, n - 2))

                a3, a2, a1, a0 = sol[4 * seg:4 * seg + 4]
                Yq[idx] = a3 * xv**3 + a2 * xv**2 + a1 * xv + a0

            return Yq

        if return_details:
            return S, sol, err
        return S

#---------------------------------------------------------------------------------------
# Unit 05: Ordinary Differential Equations (ODEs)
#---------------------------------------------------------------------------------------

    def euler(self, f, t0, tf, y0, n):
        if n <= 0:
            raise ValueError("n must be positive")
        t = np.linspace(float(t0), float(tf), int(n) + 1)
        y = np.zeros(int(n) + 1, dtype=float)
        y[0] = float(y0)

        h = t[1] - t[0]
        for i in range(n):
            y[i + 1] = y[i] + h * f(t[i], y[i])

        return t, y
    
    def runge_kutta_4(self, f, x0, xn, h, y0):
        if h == 0:
            raise ValueError("h must be nonzero")
        if (xn - x0) * h < 0:
            raise ValueError("h must move from x0 toward xn")

        steps = np.arange(float(x0), float(xn) + h, float(h))
        y = np.zeros(len(steps), dtype=float)

        y[0] = float(y0)
        for i in range(1, len(steps)):
            x_prev = steps[i - 1]
            y_prev = y[i - 1]
            k1 = f(x_prev, y_prev)
            k2 = f(x_prev + h / 2, y_prev + h * k1 / 2)
            k3 = f(x_prev + h / 2, y_prev + h * k2 / 2)
            k4 = f(x_prev + h, y_prev + h * k3)
            y[i] = y_prev + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6

        return steps, y


 
#---------------------------------------------------------------------------------------
# Unit 06: Non-linear Systems
#---------------------------------------------------------------------------------------

    def solve_nlsoe_with_history(self, F, x0, tolerance=1e-8, max_steps=100, h=1e-5):
        x = np.asarray(x0, dtype=float).reshape(-1)
        n = x.size

        if n == 0:
            raise ValueError("x0 must contain at least one variable")
        if max_steps <= 0:
            raise ValueError("max_steps must be positive")
        if tolerance <= 0:
            raise ValueError("tolerance must be positive")
        if h <= 0:
            raise ValueError("h must be positive")

        theta_hist = [x.copy()]
        residual_hist = []

        for i in range(1, max_steps + 1):
            Fx = np.asarray(F(x), dtype=float).reshape(-1)
            if Fx.size != n:
                raise ValueError(
                    f"F(x) must return a vector of length {n}, got {Fx.size}"
                )

            residual = np.linalg.norm(Fx, ord=2)
            residual_hist.append(residual)
            if residual < tolerance:
                iter_idx = np.arange(len(residual_hist), dtype=int)
                return x, i, 0, iter_idx, np.asarray(residual_hist, dtype=float), np.asarray(theta_hist, dtype=float)

            # Build Jacobian J where J[k, j] = dF_k/dx_j via forward differences.
            J = np.zeros((n, n), dtype=float)
            for j in range(n):
                x_plus = x.copy()
                x_plus[j] += h
                F_plus = np.asarray(F(x_plus), dtype=float).reshape(-1)
                if F_plus.size != n:
                    raise ValueError(
                        f"F(x) must return a vector of length {n}, got {F_plus.size}"
                    )
                J[:, j] = (F_plus - Fx) / h

            # Solve J * delta = -F(x) using Unit 04 linear system solver.
            try:
                delta, err = self.solve_lsoe(J, -Fx)
            except ValueError:
                iter_idx = np.arange(len(residual_hist), dtype=int)
                return x, i, -1, iter_idx, np.asarray(residual_hist, dtype=float), np.asarray(theta_hist, dtype=float)

            if err != 0:
                iter_idx = np.arange(len(residual_hist), dtype=int)
                return x, i, -1, iter_idx, np.asarray(residual_hist, dtype=float), np.asarray(theta_hist, dtype=float)

            x = x + delta
            theta_hist.append(x.copy())

        iter_idx = np.arange(len(residual_hist), dtype=int)
        return x, max_steps, -2, iter_idx, np.asarray(residual_hist, dtype=float), np.asarray(theta_hist, dtype=float)

    def solve_nlsoe(self, F, x0, tolerance=1e-8, max_steps=100):
        x, i, err, _, _, _ = self.solve_nlsoe_with_history(
            F, x0, tolerance=tolerance, max_steps=max_steps
        )
        return x, i, err

#---------------------------------------------------------------------------------------
# Consolidated compatability classes / Old unit tests
#---------------------------------------------------------------------------------------

class tools(Tools):
    """Backwards-compatible alias used by existing Unit 01/02/03 scripts."""


class IntegrationTools(Tools):
    """Compatibility class for integration workflows."""


class DifferentiationTools(Tools):
    """Compatibility class for differentiation workflows."""


        