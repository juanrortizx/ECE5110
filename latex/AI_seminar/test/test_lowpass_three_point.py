"""
Three-point numerical differentiation test for a second-order low-pass filter.

This script evaluates derivative accuracy for a standard second-order low-pass
step response and exports graphs to the plots folder.

Run:
    python scripts/test_lowpass_three_point.py
"""

import csv
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

from lib.differentiation_tools import DifferentiationTools  # noqa: E402


def step_response_lowpass_2nd_order(t, omega_n, zeta):
    """Unit-step response of a canonical underdamped second-order low-pass filter."""
    t = np.asarray(t, dtype=float)
    omega_d = omega_n * np.sqrt(1.0 - zeta**2)
    alpha = zeta / np.sqrt(1.0 - zeta**2)
    return 1.0 - np.exp(-zeta * omega_n * t) * (
        np.cos(omega_d * t) + alpha * np.sin(omega_d * t)
    )


def impulse_response_lowpass_2nd_order(t, omega_n, zeta):
    """Exact derivative of the step response (impulse response)."""
    t = np.asarray(t, dtype=float)
    omega_d = omega_n * np.sqrt(1.0 - zeta**2)
    gain = (omega_n**2) / omega_d
    return gain * np.exp(-zeta * omega_n * t) * np.sin(omega_d * t)


def main():
    tool = DifferentiationTools()

    # Typical second-order low-pass prototype settings (Butterworth-like damping)
    zeta = 1.0 / np.sqrt(2.0)
    f_n_hz = 1000.0
    omega_n = 2.0 * np.pi * f_n_hz

    # Differentiation setup
    h = 1e-6
    t_final = 6.0 / (zeta * omega_n)
    t = np.linspace(2.0 * h, t_final, 1400)

    y_exact = impulse_response_lowpass_2nd_order(t, omega_n, zeta)

    def y_step_scalar(ts):
        return float(step_response_lowpass_2nd_order(ts, omega_n, zeta))

    y_central = np.array(
        [tool.numerical_differentiation_3point(y_step_scalar, ti, h=h, method="central") for ti in t]
    )
    y_forward = np.array(
        [tool.numerical_differentiation_3point(y_step_scalar, ti, h=h, method="forward") for ti in t]
    )
    y_backward = np.array(
        [tool.numerical_differentiation_3point(y_step_scalar, ti, h=h, method="backward") for ti in t]
    )

    err_central = np.abs(y_central - y_exact)
    err_forward = np.abs(y_forward - y_exact)
    err_backward = np.abs(y_backward - y_exact)

    out_dir = PROJECT_ROOT / "plots" / "lowpass_three_point"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Plot 1: exact derivative vs. numerical derivatives
    fig1, ax1 = plt.subplots(figsize=(9, 5))
    ax1.plot(t * 1e3, y_exact, "k", linewidth=2.0, label="Exact dy/dt")
    ax1.plot(t * 1e3, y_central, "--", linewidth=1.2, label="3-point central")
    ax1.plot(t * 1e3, y_forward, "-.", linewidth=1.2, label="3-point forward")
    ax1.plot(t * 1e3, y_backward, ":", linewidth=1.4, label="3-point backward")
    ax1.set_xlabel("Time [ms]")
    ax1.set_ylabel("Derivative [1/s]")
    ax1.set_title("Second-Order Low-Pass Step Response Derivative")
    ax1.grid(True, linestyle="--", linewidth=0.5)
    ax1.legend()
    fig1.tight_layout()

    # Plot 2: absolute error over time
    fig2, ax2 = plt.subplots(figsize=(9, 5))
    ax2.semilogy(t * 1e3, err_central, linewidth=1.5, label="central error")
    ax2.semilogy(t * 1e3, err_forward, linewidth=1.5, label="forward error")
    ax2.semilogy(t * 1e3, err_backward, linewidth=1.5, label="backward error")
    ax2.set_xlabel("Time [ms]")
    ax2.set_ylabel("Absolute error")
    ax2.set_title("3-Point Differentiation Error for Second-Order Low-Pass Filter")
    ax2.grid(True, which="both", linestyle="--", linewidth=0.5)
    ax2.legend()
    fig2.tight_layout()

    for ext in ("png", "svg"):
        fig1.savefig(out_dir / f"lowpass_derivative_comparison.{ext}", dpi=180, bbox_inches="tight")
        fig2.savefig(out_dir / f"lowpass_derivative_abs_error.{ext}", dpi=180, bbox_inches="tight")

    plt.close(fig1)
    plt.close(fig2)

    # Save numeric summary
    summary_rows = [
        {"method": "central", "max_abs_error": float(np.max(err_central)), "mean_abs_error": float(np.mean(err_central))},
        {"method": "forward", "max_abs_error": float(np.max(err_forward)), "mean_abs_error": float(np.mean(err_forward))},
        {"method": "backward", "max_abs_error": float(np.max(err_backward)), "mean_abs_error": float(np.mean(err_backward))},
    ]

    csv_path = out_dir / "lowpass_three_point_error_summary.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["method", "max_abs_error", "mean_abs_error"])
        writer.writeheader()
        writer.writerows(summary_rows)

    print("Saved files:")
    print(out_dir / "lowpass_derivative_comparison.png")
    print(out_dir / "lowpass_derivative_comparison.svg")
    print(out_dir / "lowpass_derivative_abs_error.png")
    print(out_dir / "lowpass_derivative_abs_error.svg")
    print(csv_path)


if __name__ == "__main__":
    main()
