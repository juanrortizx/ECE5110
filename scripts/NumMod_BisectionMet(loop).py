import math
import numpy as np
import matplotlib.pyplot as plt

# --- Use your existing functions (ensure < and > are real symbols in your code) ---
def f(x):
    if x < 0:
        raise ValueError("Sqrt must be non negative")
    return math.sqrt(x) - math.cos(x)

def bisection(func, a, b, tolerance=1e-10, max_tries=100):
    fa = func(a)
    fb = func(b)

    if fa * fb > 0:
        raise ValueError("f(a) and f(b) need opposite signs")

    hist = []
    for k in range(1, max_tries + 1):
        m = 0.5 * (a + b)
        fm = func(m)
        hist.append((a, b, m, fm))
        if abs(fm) < tolerance or 0.5 * (b - a) < tolerance:
            return m, k, hist
        if fa * fm < 0:
            b, fb = m, fm
        else:
            a, fa = m, fm
    return 0.5 * (a + b), max_tries, hist

# --- Run bisection and collect history ---
a, b = 0.0, 1.0
tol = 1e-10
root, iters, hist = bisection(f, a, b, tolerance=tol, max_tries=100)

# --- Prepare data for plotting ---
xs = np.linspace(a, b, 200)
ys = [f(x) for x in xs]

midpoints = [rec[2] for rec in hist]
f_mid = [rec[3] for rec in hist]

# --- Plot: function and midpoints ---
plt.figure(figsize=(8, 5))
plt.axhline(0, color='k', linewidth=1)
plt.plot(xs, ys, label=r'$f(x)=\sqrt{x}-\cos(x)$', color='tab:blue')

# bracket endpoints
plt.scatter([a, b], [f(a), f(b)], color='tab:orange', zorder=3, label='Endpoints')

# midpoints across iterations
plt.scatter(midpoints, f_mid, color='tab:red', s=25, zorder=4, label='Bisection midpoints')

# final root
plt.scatter([root], [f(root)], color='green', s=60, marker='X', zorder=5, label=f'Root ≈ {root:.6f}')

plt.title('Bisection on $f(x)=\\sqrt{x}-\\cos x$')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()