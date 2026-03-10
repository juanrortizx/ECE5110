from lib.tools import tools

tool = tools()

# Your data
x = [-2.0, -1.0, 0.0, 1.5, 3.0]
y = [-2.0, -4.0, 1.0, 1.7, 3.2]

# Build the Lagrange interpolant (callable)
P = tool.lagrange_interpolator(x, y)

# Choose a plotting interval (pad beyond data range if you like)
a, b = -3.0, 4.0

# Optionally, choose "solution" markers you want highlighted on the curve.
# For interpolation, you might mark the original nodes 
#   (so you can see it passes through them)
solutions = x
labels = [f"({xi}, {yi})" for xi, yi in zip(x, y)]

# Universal plot: SAME function for roots, trends, anything callable
tool.plot_solution(P, 
                   a, 
                   b, 
                   solutions=solutions, 
                   labels=labels, 
                   title="Lagrange Interpolation (Universal Plot)"
                   )


# Build Newton interpolant
N, a, nodes = tool.newton_interpolator(x, y)

# Plot using your universal plotter
a_plot, b_plot = -3.0, 4.0
solutions = x
labels = [f"({xi}, {yi})" for xi, yi in zip(x, y)]
tool.plot_solution(N, 
                   a_plot, 
                   b_plot, 
                   solutions=solutions, 
                   labels=labels,
                   title="Newton Interpolation (Universal Plot)"
                   )
