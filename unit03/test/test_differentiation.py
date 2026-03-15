import csv
import json
import shutil
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lib.differentiation_tools import DifferentiationTools

UNIT_RESULTS_DIR = PROJECT_ROOT / "unit03" / "results"

TEST_CASES = (
    {
        "name": "sine_at_pi_over_4",
        "display_name": "sin(x) at x = pi/4",
        "f": np.sin,
        "df": np.cos,
        "x": float(np.pi / 4.0),
        "h": 1e-5,
        "tolerances": {"central": 1e-8, "forward": 1e-7, "backward": 1e-7},
    },
    {
        "name": "exp_at_0p3",
        "display_name": "exp(x) at x = 0.3",
        "f": np.exp,
        "df": np.exp,
        "x": 0.3,
        "h": 1e-5,
        "tolerances": {"central": 1e-8, "forward": 1e-7, "backward": 1e-7},
    },
    {
        "name": "poly_cubic_minus_quadratic",
        "display_name": "x^3 - 2x^2 + x - 5 at x = 1.2",
        "f": lambda x: x**3 - 2.0 * x**2 + x - 5.0,
        "df": lambda x: 3.0 * x**2 - 4.0 * x + 1.0,
        "x": 1.2,
        "h": 1e-5,
        "tolerances": {"central": 1e-8, "forward": 1e-7, "backward": 1e-7},
    },
)

METHODS = ("central", "forward", "backward")
H_VALUES = np.logspace(-1, -8, 80)

FREEFALL_POSITION_DATA = np.array([0.0, -0.05, -0.10, -0.15, -0.20, -0.25, -0.30], dtype=float)
FREEFALL_TIME_DATA = np.array([0.0, 0.100764, 0.141736, 0.174306, 0.201042, 0.224583, 0.247569], dtype=float)
FREEFALL_GRAVITY_TOL = 0.15


def create_output_dirs(base_dir: Path):
    if base_dir.exists():
        shutil.rmtree(base_dir)

    article_results_dir = base_dir / "article_results"
    plots_dir = base_dir / "plots"
    article_images_dir = base_dir / "article_images"

    article_results_dir.mkdir(parents=True, exist_ok=True)
    plots_dir.mkdir(parents=True, exist_ok=True)
    article_images_dir.mkdir(parents=True, exist_ok=True)

    return base_dir, article_results_dir, plots_dir, article_images_dir


def sanitize_filename(name: str) -> str:
    cleaned = []
    previous_was_underscore = False

    for char in name.lower():
        if char.isalnum():
            cleaned.append(char)
            previous_was_underscore = False
        elif not previous_was_underscore:
            cleaned.append("_")
            previous_was_underscore = True

    sanitized = "".join(cleaned).strip("_")
    return sanitized or "table"


def build_freefall_position_interpolant():
    coeffs = np.polyfit(FREEFALL_TIME_DATA, FREEFALL_POSITION_DATA, 2)
    position_poly = np.poly1d(coeffs)
    return position_poly, FREEFALL_TIME_DATA.copy(), FREEFALL_POSITION_DATA.copy()


def estimate_gravity_from_interpolated_freefall(tool: DifferentiationTools, h: float = 1e-5):
    position_poly, time_data, position_data = build_freefall_position_interpolant()

    def velocity(t):
        return tool.numerical_differentiation_3point(position_poly, t, h=h, method="central")

    def acceleration(t):
        return tool.numerical_differentiation_3point(velocity, t, h=h, method="central")

    t0 = float(time_data[len(time_data) // 2])
    accel_est = float(acceleration(t0))
    accel_mag = abs(accel_est)
    target_g = 9.81
    abs_error = abs(accel_mag - target_g)
    passed = abs_error <= FREEFALL_GRAVITY_TOL

    return {
        "case_name": "freefall_gravity_interpolation",
        "display_name": "Free-fall gravity from quadratic interpolant",
        "interpolant_type": "quadratic (polyfit degree 2)",
        "position_units": "m",
        "time_units": "s",
        "acceleration_units": "m/s^2",
        "evaluation_time": t0,
        "step_size": float(h),
        "accel_estimate_signed": accel_est,
        "accel_estimate_magnitude": accel_mag,
        "target_gravity_magnitude": target_g,
        "magnitude_abs_error": abs_error,
        "tolerance": float(FREEFALL_GRAVITY_TOL),
        "passed": bool(passed),
        "source_time_data": time_data.tolist(),
        "source_position_data": position_data.tolist(),
        "quadratic_coefficients": position_poly.c.tolist(),
    }


def collect_results(tool: DifferentiationTools):
    rows = []

    for case in TEST_CASES:
        x = float(case["x"])
        h = float(case["h"])
        exact = float(case["df"](x))

        for method in METHODS:
            approx = float(tool.numerical_differentiation_3point(case["f"], x, h=h, method=method))
            abs_error = abs(approx - exact)
            rel_error = abs_error / max(abs(exact), np.finfo(float).eps)
            tol = float(case["tolerances"][method])

            rows.append(
                {
                    "case_name": case["name"],
                    "display_name": case["display_name"],
                    "method": method,
                    "x": x,
                    "h": h,
                    "exact": exact,
                    "approx": approx,
                    "abs_error": abs_error,
                    "rel_error": rel_error,
                    "tolerance": tol,
                    "passed": abs_error <= tol,
                }
            )

    return rows


def build_summary(rows):
    summary = []

    for method in METHODS:
        method_rows = [row for row in rows if row["method"] == method]
        abs_errors = np.array([row["abs_error"] for row in method_rows], dtype=float)
        rel_errors = np.array([row["rel_error"] for row in method_rows], dtype=float)

        summary.append(
            {
                "method": method,
                "num_cases": len(method_rows),
                "all_passed": all(row["passed"] for row in method_rows),
                "max_abs_error": float(abs_errors.max()) if len(abs_errors) else float("nan"),
                "mean_abs_error": float(abs_errors.mean()) if len(abs_errors) else float("nan"),
                "max_rel_error": float(rel_errors.max()) if len(rel_errors) else float("nan"),
                "mean_rel_error": float(rel_errors.mean()) if len(rel_errors) else float("nan"),
            }
        )

    return summary


def _markdown_table(rows, columns):
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    data_lines = []

    for row in rows:
        cells = [format_cell(row[col], col) for col in columns]
        data_lines.append("| " + " | ".join(cells) + " |")

    return "\n".join([header, separator] + data_lines)


def save_results(rows, article_results_dir: Path, freefall_result: dict):
    result_columns = [
        "case_name",
        "display_name",
        "method",
        "x",
        "h",
        "exact",
        "approx",
        "abs_error",
        "rel_error",
        "tolerance",
        "passed",
    ]
    summary = build_summary(rows)
    summary_columns = [
        "method",
        "num_cases",
        "all_passed",
        "max_abs_error",
        "mean_abs_error",
        "max_rel_error",
        "mean_rel_error",
    ]

    results_csv = article_results_dir / "differentiation_test_results.csv"
    with results_csv.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=result_columns)
        writer.writeheader()
        writer.writerows(rows)

    results_json = article_results_dir / "differentiation_test_results.json"
    with results_json.open("w", encoding="utf-8") as file:
        json.dump(rows, file, indent=2)

    results_md = article_results_dir / "differentiation_test_results.md"
    with results_md.open("w", encoding="utf-8") as file:
        file.write("# 3-Point Differentiation Test Results\n\n")
        file.write(_markdown_table(rows, result_columns) + "\n")

    summary_csv = article_results_dir / "differentiation_summary.csv"
    with summary_csv.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=summary_columns)
        writer.writeheader()
        writer.writerows(summary)

    freefall_columns = [
        "case_name",
        "display_name",
        "interpolant_type",
        "evaluation_time",
        "step_size",
        "accel_estimate_signed",
        "accel_estimate_magnitude",
        "target_gravity_magnitude",
        "magnitude_abs_error",
        "tolerance",
        "passed",
        "time_units",
        "position_units",
        "acceleration_units",
    ]
    freefall_row = {column: freefall_result[column] for column in freefall_columns}

    freefall_csv = article_results_dir / "freefall_gravity_results.csv"
    with freefall_csv.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=freefall_columns)
        writer.writeheader()
        writer.writerow(freefall_row)

    freefall_json = article_results_dir / "freefall_gravity_results.json"
    with freefall_json.open("w", encoding="utf-8") as file:
        json.dump(freefall_result, file, indent=2)

    freefall_md = article_results_dir / "freefall_gravity_results.md"
    with freefall_md.open("w", encoding="utf-8") as file:
        file.write("# Free-Fall Gravity Validation\n\n")
        file.write(
            "This result uses a quadratic interpolant of position-versus-time data, then applies "
            "the central 3-point finite-difference method twice (position -> velocity -> acceleration).\n\n"
        )
        file.write("## Gravity Estimate Summary\n\n")
        file.write(_markdown_table([freefall_row], freefall_columns) + "\n\n")
        file.write("## Source Data\n\n")
        source_rows = [
            {
                "index": idx,
                "time_s": freefall_result["source_time_data"][idx],
                "position_m": freefall_result["source_position_data"][idx],
            }
            for idx in range(len(freefall_result["source_time_data"]))
        ]
        file.write(_markdown_table(source_rows, ["index", "time_s", "position_m"]) + "\n\n")
        file.write("## Quadratic Interpolant Coefficients\n\n")
        coeff_rows = [
            {"coefficient": f"a{2 - idx}", "value": value}
            for idx, value in enumerate(freefall_result["quadratic_coefficients"])
        ]
        file.write(_markdown_table(coeff_rows, ["coefficient", "value"]) + "\n")

    metadata = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "num_analytic_cases": len(TEST_CASES),
        "num_analytic_rows": len(rows),
        "methods": list(METHODS),
        "h_values": H_VALUES.tolist(),
        "output_root": str(article_results_dir.parent),
        "gravity_case_name": freefall_result["case_name"],
        "gravity_passed": bool(freefall_result["passed"]),
    }

    metadata_json = article_results_dir / "run_metadata.json"
    with metadata_json.open("w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2)


def format_cell(value, column_name):
    _ = column_name

    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, (int, np.integer)):
        return str(int(value))
    if isinstance(value, (float, np.floating)):
        return f"{float(value):.6e}"
    return str(value)


def save_table_image(rows, columns, output_base: Path, title: str):
    cell_text = [[format_cell(row[column], column) for column in columns] for row in rows]

    fig_height = max(2.0, 1.0 + 0.45 * max(1, len(rows)))
    fig_width = max(8.0, 1.2 * len(columns))
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.axis("off")

    table = ax.table(cellText=cell_text, colLabels=columns, loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1.0, 1.25)

    ax.set_title(title, fontsize=11, pad=12)
    fig.tight_layout()
    fig.savefig(output_base.with_suffix(".png"), dpi=300, bbox_inches="tight")
    fig.savefig(output_base.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)


def generate_article_images(rows, article_images_dir: Path, freefall_result: dict):
    summary_rows = build_summary(rows)
    summary_cols = [
        "method",
        "num_cases",
        "all_passed",
        "max_abs_error",
        "mean_abs_error",
        "max_rel_error",
        "mean_rel_error",
    ]
    save_table_image(summary_rows, summary_cols, article_images_dir / "summary_table", "Method Summary")

    result_cols = [
        "case_name",
        "method",
        "x",
        "h",
        "exact",
        "approx",
        "abs_error",
        "rel_error",
        "tolerance",
        "passed",
    ]
    save_table_image(rows, result_cols, article_images_dir / "all_results_table", "All Analytic Results")

    ranked_rows = sorted(rows, key=lambda row: row["abs_error"], reverse=True)
    save_table_image(
        ranked_rows,
        result_cols,
        article_images_dir / "error_ranking_table",
        "Error Ranking (Descending Absolute Error)",
    )

    for case in TEST_CASES:
        case_rows = [row for row in rows if row["case_name"] == case["name"]]
        output_name = sanitize_filename(f"{case['name']}_results_table")
        save_table_image(
            case_rows,
            result_cols,
            article_images_dir / output_name,
            f"Results for {case['display_name']}",
        )

    freefall_row = {
        "evaluation_time": freefall_result["evaluation_time"],
        "step_size": freefall_result["step_size"],
        "accel_estimate_signed": freefall_result["accel_estimate_signed"],
        "accel_estimate_magnitude": freefall_result["accel_estimate_magnitude"],
        "target_gravity_magnitude": freefall_result["target_gravity_magnitude"],
        "magnitude_abs_error": freefall_result["magnitude_abs_error"],
        "tolerance": freefall_result["tolerance"],
        "passed": freefall_result["passed"],
    }
    save_table_image(
        [freefall_row],
        list(freefall_row.keys()),
        article_images_dir / "freefall_gravity_results_table",
        "Free-Fall Gravity Estimate",
    )

    source_rows = [
        {
            "index": idx,
            "time_s": freefall_result["source_time_data"][idx],
            "position_m": freefall_result["source_position_data"][idx],
        }
        for idx in range(len(freefall_result["source_time_data"]))
    ]
    save_table_image(
        source_rows,
        ["index", "time_s", "position_m"],
        article_images_dir / "freefall_source_data_table",
        "Free-Fall Source Data",
    )


def generate_plots(tool: DifferentiationTools, plots_dir: Path, freefall_result: dict):
    for case in TEST_CASES:
        x = float(case["x"])
        exact = float(case["df"](x))

        fig, ax = plt.subplots(figsize=(7.5, 4.8))
        for method in METHODS:
            errors = []
            for h in H_VALUES:
                approx = tool.numerical_differentiation_3point(case["f"], x, h=float(h), method=method)
                errors.append(abs(float(approx) - exact))

            ax.loglog(H_VALUES, np.array(errors), label=method)

        ax.set_xlabel("Step size h")
        ax.set_ylabel("Absolute error")
        ax.set_title(f"3-point error vs h: {case['display_name']}")
        ax.grid(True, which="both", linestyle="--", linewidth=0.6, alpha=0.5)
        ax.legend()
        fig.tight_layout()

        base_name = sanitize_filename(f"{case['name']}_error_vs_h")
        fig.savefig(plots_dir / f"{base_name}.png", dpi=300, bbox_inches="tight")
        fig.savefig(plots_dir / f"{base_name}.svg", bbox_inches="tight")
        plt.close(fig)

    position_poly, time_data, position_data = build_freefall_position_interpolant()
    t_dense = np.linspace(float(time_data.min()), float(time_data.max()), 300)
    y_dense = position_poly(t_dense)

    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    ax.plot(t_dense, y_dense, label="Quadratic interpolant", linewidth=2.0)
    ax.scatter(time_data, position_data, label="Sample data", zorder=3)

    t0 = freefall_result["evaluation_time"]
    y0 = float(position_poly(t0))
    ax.scatter([t0], [y0], label="Evaluation point", marker="x", s=90, zorder=4)

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Position (m)")
    ax.set_title(
        "Free-fall interpolation (|g_est| = "
        f"{freefall_result['accel_estimate_magnitude']:.4f} m/s^2)"
    )
    ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.5)
    ax.legend()
    fig.tight_layout()

    fig.savefig(plots_dir / "freefall_gravity_interpolation.png", dpi=300, bbox_inches="tight")
    fig.savefig(plots_dir / "freefall_gravity_interpolation.svg", bbox_inches="tight")
    plt.close(fig)


def _write_unittest_report(rows, article_results_dir: Path, freefall_result: dict):
    summary_rows = build_summary(rows)

    analytic_ok = all(row["passed"] for row in rows)
    gravity_ok = bool(freefall_result["passed"])
    overall_ok = analytic_ok and gravity_ok

    lines = [
        "Unit 03 Differentiation Report",
        "=" * 34,
        "",
        "Analytic Summary (per method):",
        "method | num_cases | all_passed | max_abs_error | mean_abs_error | max_rel_error | mean_rel_error",
    ]

    for row in summary_rows:
        lines.append(
            "{method} | {num_cases} | {all_passed} | {max_abs_error:.6e} | {mean_abs_error:.6e} | "
            "{max_rel_error:.6e} | {mean_rel_error:.6e}".format(**row)
        )

    lines.extend(
        [
            "",
            "Gravity Check Summary:",
            f"evaluation_time_s: {freefall_result['evaluation_time']:.6e}",
            f"estimated_signed_accel_mps2: {freefall_result['accel_estimate_signed']:.6e}",
            f"estimated_accel_magnitude_mps2: {freefall_result['accel_estimate_magnitude']:.6e}",
            f"target_abs_g_mps2: {freefall_result['target_gravity_magnitude']:.6e}",
            f"magnitude_abs_error: {freefall_result['magnitude_abs_error']:.6e}",
            f"tolerance: {freefall_result['tolerance']:.6e}",
            f"pass: {freefall_result['passed']}",
            "",
            f"overall_analytic_status: {analytic_ok}",
            f"overall_gravity_status: {gravity_ok}",
            f"overall_combined_status: {overall_ok}",
            "",
        ]
    )

    report_path = article_results_dir / "unittest_report.txt"
    report_path.write_text("\n".join(lines), encoding="utf-8")


class TestDifferentiationThreePoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool = DifferentiationTools()
        cls.output_root, cls.article_results_dir, cls.plots_dir, cls.article_images_dir = create_output_dirs(UNIT_RESULTS_DIR)
        cls.rows = collect_results(cls.tool)
        cls.freefall_result = estimate_gravity_from_interpolated_freefall(cls.tool)

        save_results(cls.rows, cls.article_results_dir, cls.freefall_result)
        generate_article_images(cls.rows, cls.article_images_dir, cls.freefall_result)
        generate_plots(cls.tool, cls.plots_dir, cls.freefall_result)
        _write_unittest_report(cls.rows, cls.article_results_dir, cls.freefall_result)

    def test_all_methods_meet_tolerance(self):
        failures = [
            row
            for row in self.rows
            if not row["passed"]
        ]

        if failures:
            details = [
                (
                    f"case={row['case_name']}, method={row['method']}, "
                    f"abs_error={row['abs_error']:.6e}, tol={row['tolerance']:.6e}"
                )
                for row in failures
            ]
            self.fail("Analytic tolerance failures:\n" + "\n".join(details))

    def test_gravity_from_interpolated_freefall_data(self):
        accel_est = float(self.freefall_result["accel_estimate_signed"])
        self.assertAlmostEqual(abs(accel_est), 9.81, delta=FREEFALL_GRAVITY_TOL)

    def test_invalid_method_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.tool.numerical_differentiation_3point(np.sin, 0.1, h=1e-5, method="invalid")

    def test_nonpositive_h_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.tool.numerical_differentiation_3point(np.sin, 0.1, h=0.0, method="central")


if __name__ == "__main__":
    unittest.main(verbosity=2)
