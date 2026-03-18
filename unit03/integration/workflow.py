"""Orchestration for Unit 03 integration outputs."""

from datetime import datetime, timezone

from .artifacts import prepare_output_dirs, write_method_outputs, write_unittest_report
from .calculators import build_summary, collect_method_results
from .config import BENCHMARK_CASES, EXPECTED_ORDERS, MIN_OBSERVED_ORDERS
from .visuals import generate_article_images, generate_error_plots

CASE_BY_NAME = {case["name"]: case for case in BENCHMARK_CASES}


def _run_method(tool, method_key, output_dirs):
    rows, case_orders = collect_method_results(tool, method_key)
    summary_rows = build_summary(
        rows,
        case_orders,
        method_key,
        min_order=MIN_OBSERVED_ORDERS[method_key],
    )

    all_accuracy_pass = all(
        _case_accuracy_pass(row, method_key) for row in rows if row["n"] == max(r["n"] for r in rows)
    )
    all_order_pass = all(
        case_orders[name] >= MIN_OBSERVED_ORDERS[method_key] for name in case_orders
    )
    metadata = {
        "method": method_key,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "expected_order": EXPECTED_ORDERS[method_key],
        "minimum_required_order": MIN_OBSERVED_ORDERS[method_key],
        "observed_order_by_case": case_orders,
        "all_accuracy_pass": all_accuracy_pass,
        "all_order_pass": all_order_pass,
    }

    write_method_outputs(method_key, rows, summary_rows, metadata)
    generate_article_images(method_key, rows, summary_rows, output_dirs["article_images"])
    generate_error_plots(method_key, rows, output_dirs["plots"])

    return {
        "rows": rows,
        "summary_rows": summary_rows,
        "metadata": metadata,
        "case_orders": case_orders,
        "all_accuracy_pass": all_accuracy_pass,
        "all_order_pass": all_order_pass,
    }


def _case_accuracy_pass(row, method_key):
    case = CASE_BY_NAME[row["case_name"]]
    tol_key = "trapezoidal_tol" if method_key == "trapezoidal" else "simpson_tol"
    return row["abs_error"] <= case[tol_key]


def generate_all_outputs(tool, clear_results=True):
    """Run full integration workflow for trapezoidal and Simpson methods."""
    output_dirs = prepare_output_dirs(clear_results=clear_results)

    method_outputs = {
        "trapezoidal": _run_method(tool, "trapezoidal", output_dirs),
        "simpson": _run_method(tool, "simpson", output_dirs),
    }
    report_path = write_unittest_report(method_outputs)

    return {
        "trapezoidal": method_outputs["trapezoidal"],
        "simpson": method_outputs["simpson"],
        "output_dirs": output_dirs,
        "report_path": report_path,
    }
