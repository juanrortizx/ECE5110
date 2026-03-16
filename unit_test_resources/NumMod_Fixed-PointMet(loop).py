import math
import numpy as np
import matplotlib.pyplot as plt

def f(x):
    """Fixed-Point map: x_{n+1} = cos^2(x_n)"""
    c = math.cos(x) * math.cos(x)
    return c

def fixed_point(f, x0, tolerance = 1e-8, max_steps = 1000):
    x = x0
    history = []
    
    for k in range(1, max_steps + 1):
        fx = f(x)
        residual = abs(x - fx)
        
        if residual < tolerance:
            return fx, k, history, True
    
        x = fx

    return x, max_steps, history, False

# --- Run fixed-point iteration and collect history ---

x0 = 0.5
tol = 1e-8

root, iters, hist, ok = fixed_point(f, x0=x0,tolerance = tol, max_steps=1000)


#print(f"Converged: {ok}, iterations: {iters}, root ≈ {root:.12f}, final residual ≈ {abs(root - f(root)):.3e}")

# -----------------------------
# Prepare data for plotting
# -----------------------------
# Phase plot: y = f(x) and y = x over a plausible interval, e.g., [0,1]
a, b = 0.0, 1.0
xs = np.linspace(a, b, 400)
ys = [f(x) for x in xs]
'''
# Extract iteration history for plotting
ks = [rec[0] for rec in hist]
xn = [rec[1] for rec in hist]      # x_n before update
fxn = [rec[2] for rec in hist]     # f(x_n) = x_{n+1}
res = [rec[3] for rec in hist]     # |x_n - f(x_n)|
'''
# -----------------------------
# Plot 1: Phase diagram (y = f(x)) with y = x and the iteration "cobweb" path
# -----------------------------
plt.figure(figsize=(7.5, 5.3))
plt.plot(xs, ys, label=r'$f(x)=\cos^2 x$', color='tab:blue')
plt.plot(xs, xs, label=r'$y=x$', color='k', linestyle='--', linewidth=1)
'''
# Cobweb plot (x_n, f(x_n)) and (f(x_n), f(x_n)) steps
if len(xn) > 0:
    # Draw the cobweb lines
    cx = x0
    for k in range(min(len(xn), 100)):  # limit clutter if many iterations
        fx = f(cx)
        # vertical: (cx, cx) -> (cx, f(cx))
        plt.plot([cx, cx], [cx, fx], color='tab:red', alpha=0.7)
        # horizontal: (cx, f(cx)) -> (f(cx), f(cx))
        plt.plot([cx, fx], [fx, fx], color='tab:red', alpha=0.7)
        cx = fx
'''
# Mark the final root
plt.scatter([root], [f(root)], color='green', s=60, marker='X', zorder=5, label=fr'Root ≈ {root:.6f}')
plt.title('Fixed-Point Iteration for $x = \\cos^2 x$ (solves $\\sqrt{x} - \\cos x = 0$)')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# -----------------------------
# Plot 2: Residual vs iteration
# -----------------------------
'''
plt.figure(figsize=(7.5, 4.6))
plt.semilogy(ks, res, marker='o', color='tab:purple')
plt.title(r'Residual $|x_n - f(x_n)|$ vs Iteration')
plt.xlabel('Iteration n')
plt.ylabel(r'$|x_n - f(x_n)|$ (log scale)')
plt.grid(True, which='both', alpha=0.3)
plt.tight_layout()
'''

plt.show()
