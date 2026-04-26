import sys
import numpy as np
from pathlib import Path


# Add parent directory to path so we can import from lib
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.tools import Tools # Tool Functions
tool = Tools() 
from lib.helper import Helper # Plot Functions
helper = Helper()


# Your data
x = [-2.0, -1.0, 0.0, 1.5, 3.0]
y = [-2.0, -4.0, -8.0, 1.7, 3.2]

# Build the Lagrange interpolant (callable)
P = tool.lagrange_interpolator(x, y)

# Use knot range for fair interpolation/spline comparison.
a, b = min(x), max(x)

# Optionally, choose "solution" markers you want highlighted on the curve.
# For interpolation, you might mark the original nodes 
#   (so you can see it passes through them)
solutions = x
labels = "Lagrange"

# Universal plot: SAME function for roots, trends, anything callable
helper.plot_solution(P, 
                   a, 
                   b, 
                   solutions=solutions, 
                   labels=labels, 
                   title="Lagrange Interpolation (Universal Plot)"
                   )


# Build Newton interpolant
N, _, nodes = tool.newton_interpolator(x, y)

# Plot using your universal plotter
a_plot, b_plot = min(x), max(x)
solutions = x
labels = "Newton"
helper.plot_solution(N, 
                   a_plot, 
                   b_plot, 
                   solutions=solutions, 
                   labels=labels,
                   title="Newton Interpolation (Universal Plot)"
                   )

# Build Cubic Spline interpolant
S = tool.cubic_splines(x, y)

# Plot using your universal plotter
a_plot, b_plot = min(x), max(x)
solutions = x
labels = "Cubic Spline"
helper.plot_solution(S, 
                   a_plot, 
                   b_plot, 
                   solutions=solutions, 
                   labels=labels,
                   title="Cubic Spline Interpolation (Universal Plot)"
                   )