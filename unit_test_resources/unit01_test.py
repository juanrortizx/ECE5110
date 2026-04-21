import sys
import numpy as np
from pathlib import Path


# Add parent directory to path so we can import from lib
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.tools import Tools # Tool Functions
tool = Tools() 
from lib.helper import Helper # Plot Functions
helper = Helper()


# Solve one-variable nonlinear equation: f(x) = cos(x) - x = 0
def f(x):
	return np.cos(x) - x


# Fixed-point form for the same equation: x = g(x)
def g(x):
	return np.cos(x)


def df(x):
	return -np.sin(x) - 1


# Bisection method
root_bis, err_bis = tool.solve_bisection_loop(f, a=0.0, b=1.0, precision=1e-8, max_steps=200)

# Fixed-point method
root_fp, iter_fp, err_fp = tool.solve_fixed_point(g, x0=0.5, tolerance=1e-8, max_steps=200)

# Newton method
root_newton, iter_newton, err_newton = tool.solve_newton_method(f, df, x0=0.5, tolerance=1e-8, max_steps=50)

print("Bisection:", root_bis, "err=", err_bis)
print("Fixed Point:", root_fp, "iters=", iter_fp, "err=", err_fp)
print("Newton:", root_newton, "iters=", iter_newton, "err=", err_newton)


# Plot 1: Bisection result
helper.plot_solution(
	funcs=f,
	a=0.0,
	b=1.0,
	solutions=[root_bis],
	labels="f(x) = cos(x) - x",
	title="Unit01 Bisection Solution",
	save_path="plots/unit01_bisection_solution.png",
)

# Plot 2: Fixed-point result
helper.plot_solution(
	funcs=f,
	a=0.0,
	b=1.0,
	solutions=[root_fp],
	labels="f(x) = cos(x) - x",
	title="Unit01 Fixed Point Solution",
	save_path="plots/unit01_fixed_point_solution.png",
)

# Plot 3: Newton result
helper.plot_solution(
	funcs=f,
	a=0.0,
	b=1.0,
	solutions=[root_newton],
	labels="f(x) = cos(x) - x",
	title="Unit01 Newton Solution",
	save_path="plots/unit01_newton_solution.png",
)

