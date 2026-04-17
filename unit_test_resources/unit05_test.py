import sys
from pathlib import Path


# Add parent directory to path so we can import from lib
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.tools import Tools # Tool Functions
tool = Tools() 
from lib.helper import Helper # Plot Functions
helper = Helper()

def f(x, y):
    return x*x - y

x0 = 0
xn = 2
h = 0.001
y0 = 1

t, y = tool.runge_kutta_4(f, x0=x0, xn=xn, h=h, y0=y0)

print("t:", t)
print("y:", y)

helper.plot_solution((t, y), labels="RK4 Solution", title="ODE Trajectory")

