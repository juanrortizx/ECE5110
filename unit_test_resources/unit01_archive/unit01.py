import sys
import math
from pathlib import Path


# Add parent directory to path so we can import from lib
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.tools import Tools # Tool Functions
tool = Tools() 
from lib.helper import Helper # Plot Functions
helper = Helper()

precision = 1e-9
start = 1e-9
stop = 1e-7
max_steps = 20

def f(C):
    return 1/(2*math.pi*10000*C) - 1000

def df(C):
    return -1/(2*math.pi*10000*C**2)

tool = Tools()

sol_newton, iters_newton, err_newton = tool.solve_newton_method(
    f,
    df,
    x0=1e-8,          # better initial guess, near 1.6e-8
    tolerance=precision,
    max_steps=max_steps
)

print("root =", sol_newton, "error =", err_newton)

tool.plot_solution(
    f,
    start,
    stop,
    solutions=[sol_newton],
    labels=[f"Root: {sol_newton:.3e}"],
    title="Solution using Newton's Method"
)


print("DONE")


