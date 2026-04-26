import sys
import numpy as np
from pathlib import Path


# Add parent directory to path so we can import from lib
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.tools import Tools # Tool Functions
tool = Tools() 
from lib.helper import Helper # Plot Functions
helper = Helper()


def f_int(x):
    return np.exp(x)


def f1(x):
    return x**2

# Exact references
xact_f1_i = np.e - 1.0  # ∫ exp(x) dx from 0 to 1
xact_f1_d = 2.0    # d/dx x² at x=1

# -------------------------------
# Integration: error vs h
# -------------------------------
n_values = np.array([4, 8, 16, 32, 64, 128, 256], dtype=int)
h_int = 1.0 / n_values

err_midpoint = []
err_trapezoidal = []
err_simpsons = []

for n in n_values:
    v_mid = tool.midpoint_rule(f_int, 0, 1, int(n))
    v_trap = tool.trapezoidal_rule(f_int, 0, 1, int(n))
    v_simp = tool.simpsons_rule(f_int, 0, 1, int(n))
    err_midpoint.append(abs(v_mid - xact_f1_i))
    err_trapezoidal.append(abs(v_trap - xact_f1_i))
    err_simpsons.append(abs(v_simp - xact_f1_i))

err_midpoint = np.asarray(err_midpoint, dtype=float)
err_trapezoidal = np.asarray(err_trapezoidal, dtype=float)
err_simpsons = np.asarray(err_simpsons, dtype=float)

print("Integration errors at highest n:")
print("  Midpoint:", err_midpoint[-1])
print("  Trapezoidal:", err_trapezoidal[-1])
print("  Simpsons:", err_simpsons[-1])

# Plot log10(error) vs log10(h) for integration methods
helper.plot_solution(
    funcs=[
        (np.log10(h_int), np.log10(np.maximum(err_midpoint, 1e-16))),
        (np.log10(h_int), np.log10(np.maximum(err_trapezoidal, 1e-16))),
        (np.log10(h_int), np.log10(np.maximum(err_simpsons, 1e-16))),
    ],
    labels=["Midpoint", "Trapezoidal", "Simpsons"],
    title="Unit03 Integration Convergence",
    show_zero_line=False,
    save_path="plots/unit03_integration_methods.png",
    markers=["o", "s", "^"]
)

# -------------------------------
# Differentiation: error vs h
# -------------------------------
h_diff = np.logspace(-1, -8, 40)
x_eval = 1.0

err_central = []
err_forward = []
err_backward = []

for h in h_diff:
    d_c = tool.numerical_differentiation_3point(f1, x_eval, h=float(h), method='central')
    d_f = tool.numerical_differentiation_3point(f1, x_eval, h=float(h), method='forward')
    d_b = tool.numerical_differentiation_3point(f1, x_eval, h=float(h), method='backward')
    err_central.append(abs(d_c - xact_f1_d))
    err_forward.append(abs(d_f - xact_f1_d))
    err_backward.append(abs(d_b - xact_f1_d))

err_central = np.asarray(err_central, dtype=float)
err_forward = np.asarray(err_forward, dtype=float)
err_backward = np.asarray(err_backward, dtype=float)

print("Differentiation errors at smallest h:")
print("  Central:", err_central[-1])
print("  Forward:", err_forward[-1])
print("  Backward:", err_backward[-1])

# Plot log10(error) vs log10(h) for differentiation methods
helper.plot_solution(
    funcs=[
        (np.log10(h_diff), np.log10(np.maximum(err_central, 1e-16))),
        (np.log10(h_diff), np.log10(np.maximum(err_forward, 1e-16))),
        (np.log10(h_diff), np.log10(np.maximum(err_backward, 1e-16))),
    ],
    labels=["Central", "Forward", "Backward"],
    title="Unit03 Differentiation Convergence",
    show_zero_line=False,
    save_path="plots/unit03_differentiation_methods.png",
    markers=["o", "s", "^"]
)



