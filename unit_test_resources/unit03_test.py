import sys
from pathlib import Path

# Add parent directory to path so we can import from lib
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.tools import tools
tool = tools()

def f1(x):
    return x**2

xact_f1_i = 1/3  # ∫ x² dx from 0 to 1 is 1/3
xact_f1_d = 2 # Derivative of x² is 2x, at x=1 should be 2

# Integration methods
f1_mp = tool.midpoint_rule(f1, 0, 1, 10000)
f1_trap = tool.trapezoidal_rule(f1, 0, 1, 10000)
f1_simpson = tool.simpsons_rule(f1, 0, 1, 10000)

print("∫ x² - Midpoint Rule: ", f1_mp, " (Error: ", abs(f1_mp - xact_f1_i), ")")
print("∫ x² - Trapezoidal Rule: ", f1_trap, " (Error: ", abs(f1_trap - xact_f1_i), ")")
print("∫ x² - Simpson's Rule: ", f1_simpson, " (Error: ", abs(f1_simpson - xact_f1_i), ")")
print("Exact value of ∫ x² from 0 to 1: ", xact_f1_i)

# Numerical differentiation using 3-point formula
# Derivative of x^2 is 2x, at x=1 should be 2
x_eval = 1.0
deriv_central = tool.numerical_differentiation_3point(f1, x_eval, h=1e-5, method='central')
deriv_forward = tool.numerical_differentiation_3point(f1, x_eval, h=1e-5, method='forward')
deriv_backward = tool.numerical_differentiation_3point(f1, x_eval, h=1e-5, method='backward')

print("\nNumerical Differentiation of x² at x=1:")
print(f"Central difference: {deriv_central}", f" (Error: {abs(deriv_central - xact_f1_d)})")
print(f"Forward difference: {deriv_forward}", f" (Error: {abs(deriv_forward - xact_f1_d)})")
print(f"Backward difference: {deriv_backward}", f" (Error: {abs(deriv_backward - xact_f1_d)})")
print(f"Exact derivative (2x): {2 * x_eval}")

