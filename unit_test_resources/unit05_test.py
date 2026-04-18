import sys
import numpy as np
from pathlib import Path


# Add parent directory to path so we can import from lib
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.tools import Tools # Tool Functions
tool = Tools() 
from lib.helper import Helper # Plot Functions
helper = Helper()

def f(t, y):
    T_ambient = 20.0   # °C
    T_set = 80.0       # °C (desired temperature)
    a = 0.1            # cooling constant
    Kp = 0.5           # proportional gain

    process_noise = np.random.normal(0.0, 0.2)  # smaller than sensor noise

    return -a * (y - T_ambient) + Kp * (T_set - y)


t, y = tool.runge_kutta_4(f, x0=0.5, xn=15, h=0.05, y0=0.0)

# Generate Gaussian noise
noise_std = 0.6  # adjust this (higher = noisier)
noise = np.random.normal(loc=0.0, scale=noise_std, size=len(y))

# Add noise to the "measured" signal
y_noisy = y + noise

print("y (clean):", y)
print("y (noisy):", y_noisy)

helper.plot_solution(
    (t, y_noisy),
    labels="RK4 Noisy Sensor",
    title="ODE with Sensor Noise",
    save_path="plots/unit05_rk4_noisy.png"
)
