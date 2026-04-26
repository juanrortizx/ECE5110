import sys
import numpy as np
from pathlib import Path


# Add parent directory to path so we can import from lib
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.tools import Tools # Tool Functions
tool = Tools() 
from lib.helper import Helper # Plot Functions
helper = Helper()


# Linear system:
#   2x + y = 5
#   x - y = 1
A = np.array([[2.0, 1.0],
			  [1.0, -1.0]], dtype=float)
B = np.array([5.0, 1.0], dtype=float)

sol, err = tool.solve_lsoe(A, B)
if err != 0:
	raise RuntimeError("solve_lsoe failed")

x_sol, y_sol = sol
residual = A @ sol - B

print("Solution [x, y]:", sol)
print("Residual (A@x - B):", residual)


# Build equation lines in y(x) form for plotting.
def eq1(x):
	return 5.0 - 2.0 * x          # 2x + y = 5


def eq2(x):
	return x - 1.0                # x - y = 1 -> y = x - 1


helper.plot_solution(
	funcs=[eq1, eq2],
	a=-1.0,
	b=4.0,
	solutions={"x": [x_sol], "y": [y_sol], "labels": ["LSOE intersection"]},
	labels=["2x + y = 5", "x - y = 1"],
	title="Unit04 LSOE: Line Intersection",
	save_path="plots/unit04_lsoe_line_intersection.png",
	show_zero_line=False,
)

