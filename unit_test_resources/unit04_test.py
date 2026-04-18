import sys
import numpy as np
from pathlib import Path


# Add parent directory to path so we can import from lib
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.tools import Tools # Tool Functions
tool = Tools() 
from lib.helper import Helper # Plot Functions
helper = Helper()

# Robot parameters
L1 = 1.0  # Length of first link
L2 = 1.0  # Length of second link

# Target position
target_x = 1.2
target_y = 0.5

def f(theta):
    t1, t2 = theta
    return np.array([L1*np.cos(t1) + L2*np.cos(t1 + t2) - target_x,
                     L1*np.sin(t1) + L2*np.sin(t1 + t2) - target_y])

x0 = [0.5, 0.5]  # Initial guess for joint angles

sol, steps, err, iters, residual_hist, theta_hist = tool.solve_nlsoe_with_history(f, x0)

print("Solution (theta1, theta2):", sol)
print("Steps taken:", steps)
print("Final error:", err)

# Plot convergence of nonlinear solve (use semilog data transform for clarity).
helper.plot_solution(
    funcs=(iters, np.log10(np.maximum(residual_hist, 1e-16))),
    labels="log10(||F(theta)||2)",
    title="NLSOE Convergence History",
    markers='o',
    show_zero_line=False,
    save_path="plots/unit04_nlsoe_convergence.png"
)

# Plot joint-angle evolution across iterations (not just final values).
helper.plot_solution(
    funcs=[(iters, theta_hist[:len(iters), 0]), (iters, theta_hist[:len(iters), 1])],
    labels=["theta1", "theta2"],
    title="NLSOE State Trajectory",
    markers=['o', 's'],
    show_zero_line=False,
    save_path="plots/unit04_nlsoe_state_trajectory.png"
)