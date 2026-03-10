from lib.tools_prof import tools
import matplotlib.pyplot as plt
import numpy as np

tool = tools()

x = np.array([-2.0, -1.0, 0.0, 1.5, 3.0])
y = np.array([-2.0, -4.0, 1.0, 1.7, 3.2])

coeffs, err = tool.lagrange_interpolate(x, y)

# Plot
xx = np.linspace(min(x) - 0.5, max(x) + 0.5, 600)
yy = np.polyval(coeffs, xx)

plt.figure(figsize=(8, 5))
plt.plot(xx, yy, label='Lagrange Interpolating')
plt.scatter(x, y, color='#dd2222', label='Data')
plt.grid(True, ls='--', lw=0.6)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Lagrange interpolation')

plt.legend()
plt.show()

print("Coefficients:")
print(coeffs)

print("DONE")