import sys
import numpy as np
from pathlib import Path


# Add parent directory to path so we can import from lib
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.tools import Tools # Tool Functions
tool = Tools() 
from lib.helper import Helper # Plot Functions
helper = Helper()

Array1 = [[3, 2, -4], [2, 3, 3], [5, -3, 1]]
Array2 = [3, 15, 14]

sol, err = tool.solve_lsoe(Array1, Array2)

print("Solution:", sol)
print("Error:", err)

# LSOE gives a discrete solution vector, so plot value vs variable index.
helper.plot_solution((np.arange(1, len(sol)+1), sol), labels="LSOE Solution", title="LSOE Solution Vector")

# Optional diagnostic: residual should be near zero for a valid solve.
A = np.asarray(Array1, dtype=float)
B = np.asarray(Array2, dtype=float)
residual = A @ sol - B
helper.plot_solution(
	funcs=(np.arange(1, len(sol)+1), residual),
	labels="Residual (A@x - B)",
	title="Unit04 LSOE Residual"
)

