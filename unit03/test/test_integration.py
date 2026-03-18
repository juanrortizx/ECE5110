import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lib.integration_tools import IntegrationTools
from unit03.integration import config
from unit03.integration.artifacts import sanitize_filename
from unit03.integration.workflow import generate_all_outputs


class TestIntegrationMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool = IntegrationTools()
        cls.generated = generate_all_outputs(cls.tool)

    def test_trapezoidal_final_accuracy(self):
        failures = [
            row for row in self.generated["trapezoidal_summary_rows"] if not row["passed_final_tolerance"]
        ]
        self.assertFalse(failures, msg=f"Trapezoidal tolerance failures: {failures}")

    def test_simpson_final_accuracy(self):
        failures = [row for row in self.generated["simpson_summary_rows"] if not row["passed_final_tolerance"]]
        self.assertFalse(failures, msg=f"Simpson tolerance failures: {failures}")

    def test_observed_orders(self):
        for row in self.generated["trapezoidal_summary_rows"]:
            self.assertGreater(row["observed_order"], config.TRAPEZOIDAL_ORDER_TARGET - 0.2)
        for row in self.generated["simpson_summary_rows"]:
            self.assertGreater(row["observed_order"], config.SIMPSON_ORDER_TARGET - 0.2)

    def test_required_outputs_exist(self):
        expected_paths = [
            config.ARTICLE_RESULTS_DIR / "integration_trapezoidal_results.csv",
            config.ARTICLE_RESULTS_DIR / "integration_trapezoidal_results.json",
            config.ARTICLE_RESULTS_DIR / "integration_trapezoidal_results.md",
            config.ARTICLE_RESULTS_DIR / "integration_trapezoidal_summary.csv",
            config.ARTICLE_RESULTS_DIR / "integration_trapezoidal_metadata.json",
            config.ARTICLE_RESULTS_DIR / "integration_simpson_results.csv",
            config.ARTICLE_RESULTS_DIR / "integration_simpson_results.json",
            config.ARTICLE_RESULTS_DIR / "integration_simpson_results.md",
            config.ARTICLE_RESULTS_DIR / "integration_simpson_summary.csv",
            config.ARTICLE_RESULTS_DIR / "integration_simpson_metadata.json",
            config.ARTICLE_RESULTS_DIR / "integration_unittest_report.txt",
        ]

        for method in ("trapezoidal", "simpson"):
            for case in config.BENCHMARK_CASES:
                base = f"integration_{method}_{sanitize_filename(case['case_name'])}_error_vs_h"
                expected_paths.append(config.PLOTS_DIR / f"{base}.png")
                expected_paths.append(config.PLOTS_DIR / f"{base}.svg")

            for table in ("results_table", "summary_table"):
                base = config.ARTICLE_IMAGES_DIR / f"integration_{method}_{table}"
                expected_paths.append(base.with_suffix(".png"))
                expected_paths.append(base.with_suffix(".svg"))

        missing = [str(path) for path in expected_paths if not path.exists()]
        self.assertFalse(missing, msg="Missing expected output files:\n" + "\n".join(missing))

    def test_trapezoidal_validation(self):
        case = config.BENCHMARK_CASES[0]
        with self.assertRaises(TypeError):
            self.tool.composite_trapezoidal(123, case["a"], case["b"], 4)
        with self.assertRaises(ValueError):
            self.tool.composite_trapezoidal(case["f"], case["a"], case["b"], 0)
        with self.assertRaises(ValueError):
            self.tool.composite_trapezoidal(case["f"], case["a"], case["a"], 4)

    def test_simpson_validation(self):
        case = config.BENCHMARK_CASES[0]
        with self.assertRaises(TypeError):
            self.tool.composite_simpson(None, case["a"], case["b"], 4)
        with self.assertRaises(ValueError):
            self.tool.composite_simpson(case["f"], case["a"], case["b"], 0)
        with self.assertRaises(ValueError):
            self.tool.composite_simpson(case["f"], case["a"], case["b"], 3)
        with self.assertRaises(ValueError):
            self.tool.composite_simpson(case["f"], case["a"], case["a"], 4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
