---
name: differentiation-3point
description: "Generate or update the Unit 03 3-point differentiation workflow used in this repository. Use when maintaining lib/differentiation_tools.py, unit03/differentiation/* helpers, unit03/test/test_differentiation.py, free-fall gravity validation, and differentiation artifact exports under unit03/results/."
argument-hint: 'Task description (for example: "update 3-point differentiation tolerances", "add differentiation artifact export", or "adjust free-fall gravity validation output")'
---

# 3-Point Numerical Differentiation Skill

## When to Use

Use this skill when the task involves:

- `DifferentiationTools.numerical_differentiation_3point(...)`
- Unit 03 differentiation helper modules in `unit03/differentiation/`
- `unit03/test/test_differentiation.py` unittest orchestration
- Free-fall quadratic interpolation and gravity estimation
- Differentiation artifact, plot, and article image generation

This skill is repository-specific and should follow the current modular Unit 03 workflow.

## Layered Skill Model

Use this domain skill together with `unit03-workflow-infra` when a change touches shared path/artifact/table-image infrastructure.

- `differentiation-3point`: numerical differentiation behavior, tolerances, free-fall validation, and differentiation-specific outputs.
- `unit03-workflow-infra`: shared path setup, artifact I/O helpers, and common table-image rendering used by multiple Unit 03 domains.

### Helper Package Layout

Differentiation workflow modules are:

```text
unit03/differentiation/
  config.py        # constants + test definitions + free-fall arrays
  calculators.py   # analytic rows + free-fall gravity estimate
  artifacts.py     # CSV/JSON/Markdown/metadata/report exports
  visuals.py       # differentiation plots + article table images
  workflow.py      # generate_all_outputs(tool) orchestrator
```

Cross-domain shared helpers live in:

```text
unit03/common/
  paths.py
  artifact_io.py
  table_images.py
```

`unit03/test/test_differentiation.py` should remain a thin unittest harness that imports constants from `config.py` and uses `workflow.generate_all_outputs(...)`.

## Current Contract

- Library kernel: `lib/differentiation_tools.py`
- Workflow package: `unit03/differentiation/`
- Test harness: `unit03/test/test_differentiation.py`
- Output root: `unit03/results/`

Directory setup behavior is defined by `unit03/common/paths.py::reset_unit_results()`. It creates `article_results/`, `plots/`, and `article_images/` if missing, and does not delete existing files.

## Goal

Maintain a reproducible differentiation workflow that:

1. Evaluates three analytic derivative benchmarks with central/forward/backward 3-point stencils.
2. Estimates gravity magnitude from quadratic interpolation of free-fall samples.
3. Exports article-ready files (CSV/JSON/Markdown/TXT plus PNG/SVG tables and plots).
4. Supports direct script execution and unittest discovery.

## File 1: `lib/differentiation_tools.py`

### Required Structure

Create a class named:

```python
DifferentiationTools
```

### Required Class Docstring

Use a module/class description indicating:

- this file contains numerical differentiation methods
- plotting utilities are intentionally excluded
- plotting belongs in the test/demo script

### Required Method

Implement this public method:

```python
numerical_differentiation_3point(self, f, x, h=1e-5, method="central")
```

### Required Behavior

This method must approximate the first derivative using 3-point finite-difference formulas.

Supported methods:

- `central`
- `forward`
- `backward`

Formulas:

```python
central  = (f(x + h) - f(x - h)) / (2 * h)
forward  = (-3 * f(x) + 4 * f(x + h) - f(x + 2 * h)) / (2 * h)
backward = (f(x - 2 * h) - 4 * f(x - h) + 3 * f(x)) / (2 * h)
```

### Validation Rules

- Raise `ValueError` if `h <= 0`
- Raise `ValueError` if `method` is not one of:
  - `"central"`
  - `"forward"`
  - `"backward"`

### Style Requirements

- Keep implementation minimal and readable.
- Keep plotting/reporting logic out of this file.
- Preserve existing class and method names used by Unit 03 helpers.

## File 2: `unit03/test/test_differentiation.py`

### Purpose

This file is a thin unittest harness that calls `workflow.generate_all_outputs(...)` in `setUpClass` and then asserts on returned data and required files.

### Import Expectations

Current script behavior:

- Adds project root to `sys.path`.
- Imports `DifferentiationTools` from `lib/differentiation_tools.py`.
- Imports constants from `unit03.differentiation.config`.
- Imports `generate_all_outputs` from `unit03.differentiation.workflow`.

### Constants

Core constants are owned by `unit03/differentiation/config.py`:

- `METHODS = ("central", "forward", "backward")`
- `H_VALUES = np.logspace(-1, -8, 80)`
- `TEST_CASES` (sin, exp, cubic)
- `FREEFALL_POSITION_DATA`, `FREEFALL_TIME_DATA`, `FREEFALL_GRAVITY_TOL`

### Required Analytic Test Cases

Include exactly these three analytic cases unless the user explicitly requests changes:

1. `sin(x)` at `x = pi/4`
2. `exp(x)` at `x = 0.3`
3. `x^3 - 2x^2 + x - 5` at `x = 1.2`

Each analytic case must contain:

- internal name
- display name
- function `f`
- exact derivative `df`
- evaluation point `x`
- default `h`
- per-method tolerances

### Required Methods List

Use:

```python
METHODS = ("central", "forward", "backward")
```

### Required Step-Size Sweep

Use a log-spaced step-size array for plotting:

```python
H_VALUES = np.logspace(-1, -8, 80)
```

## Additional Required Data-Driven Gravity Validation

In addition to the three analytic cases, include one separate data-driven unit test that estimates gravitational acceleration from a free-fall position-vs-time dataset.

Use exactly these arrays:

```python
FREEFALL_POSITION_DATA = np.array([0.0, -0.05, -0.10, -0.15, -0.20, -0.25, -0.30], dtype=float)
FREEFALL_TIME_DATA = np.array([0.0, 0.100764, 0.141736, 0.174306, 0.201042, 0.224583, 0.247569], dtype=float)
FREEFALL_GRAVITY_TOL = 0.15
```

Interpretation:

- `FREEFALL_POSITION_DATA` represents position/displacement in meters
- `FREEFALL_TIME_DATA` represents time in seconds
- negative position values correspond to downward motion if upward is taken as positive

Because constant-acceleration motion is quadratic in time, fit a quadratic interpolant using:

```python
coeffs = np.polyfit(FREEFALL_TIME_DATA, FREEFALL_POSITION_DATA, 2)
position_poly = np.poly1d(coeffs)
```

Then estimate acceleration by differentiating this interpolant twice using `DifferentiationTools.numerical_differentiation_3point` with the `central` method for both differentiation steps.

Use an interior evaluation time, preferably the middle sample:

```python
t0 = float(FREEFALL_TIME_DATA[len(FREEFALL_TIME_DATA) // 2])
```

Because the sign depends on the coordinate convention, the required assertion is on magnitude:

```python
self.assertAlmostEqual(abs(accel_est), 9.81, delta=FREEFALL_GRAVITY_TOL)
```

A tolerance around `0.15` is appropriate because the provided dataset is rounded and the fitted acceleration is close to, but not exactly, `9.81 m/s^2`.

## Helper Module Responsibilities

Implement and maintain the following modules.

### `unit03/differentiation/config.py`

- Declares `TEST_CASES`, `METHODS`, `H_VALUES`, `FREEFALL_POSITION_DATA`, `FREEFALL_TIME_DATA`, and `FREEFALL_GRAVITY_TOL`.
- Any change to analytic cases or constants must be reflected here so every helper uses the same data.

### `unit03/differentiation/calculators.py`

- `build_freefall_position_interpolant()` creates the quadratic interpolant from the free-fall arrays.
- `estimate_gravity_from_interpolated_freefall(tool, h)` differentiates the interpolant twice (central method, same `h`) and returns the metadata dictionary (step size, signed/magnitude estimate, tolerances, source arrays, coefficients).
- `collect_results(tool)` evaluates each analytic test case for every method, capturing exact/approximate derivatives plus absolute/relative errors and pass/fail flags.
- `build_summary(rows)` collapses rows per method and reports counts plus max/mean absolute/relative error values.

### `unit03/differentiation/artifacts.py`

- `sanitize_filename()` normalizes case-specific filenames.
- `save_results(rows, freefall_result, article_results_dir)` writes all differentiation CSV/JSON/Markdown/metadata outputs.
- `write_unittest_report(rows, freefall_result)` exports the plain-text summary (analytic + gravity sections) into `article_results/unittest_report.txt`.

### `unit03/differentiation/visuals.py`

- `generate_article_images(rows, article_images_dir, freefall_result)` produces the summary/all-results/error-ranking tables, per-case tables, and the two free-fall tables.
- `generate_plots(tool, plots_dir, freefall_result)` sweeps `H_VALUES` for each analytic case (log-log PNG/SVG) and produces the dedicated free-fall interpolation plot that overlays the data, interpolant, evaluation point, and estimated |g|.

### `unit03/differentiation/workflow.py`

- Exposes `generate_all_outputs(tool)` which:
  - calls `reset_unit_results()` via `unit03.common.paths`
  - collects analytic rows and the free-fall estimate
  - saves CSV/JSON/Markdown/metadata
  - generates article images and plots
  - writes the unittest report
  - returns the in-memory data structures so `unit03/test/test_differentiation.py` can assert on them.

### `unit03/test/test_differentiation.py`

- Imports `DifferentiationTools`, `unit03.differentiation.config`, and `unit03.differentiation.workflow`.
- In `setUpClass`, instantiates the tool and calls `workflow.generate_all_outputs(...)`.
- Stores `rows` and `freefall_result` from the workflow output for the tests listed below.
- Contains the required unittest methods only (no helper redefinitions).

## Required `unittest` Class

Create this class:

```python
class TestDifferentiationThreePoint(unittest.TestCase):
```

### `setUpClass`

In `setUpClass`, do all of the following:

- instantiate `DifferentiationTools`
- ensure the Unit 03 output directories exist inside `unit03/results`
- collect analytic result rows
- compute the free-fall gravity estimate using the interpolated dataset
- save CSV/JSON/Markdown/metadata files
- generate article images
- generate plots
- write a plain-text unit test report to:

```text
unit03/results/article_results/unittest_report.txt
```

The report should include both:

- the analytic case summary table
- a gravity-check summary containing:
  - evaluation time
  - estimated signed acceleration
  - acceleration magnitude
  - target `|g|`
  - magnitude absolute error
  - tolerance
  - pass/fail
  - overall analytic status
  - overall gravity status
  - overall combined status

### Required Tests (Current)

`TestDifferentiationThreePoint` currently verifies:

1. `test_all_methods_meet_tolerance`
2. `test_gravity_from_interpolated_freefall_data`
3. `test_required_outputs_exist`

### Main Guard

Include:

```python
if __name__ == "__main__":
    unittest.main(verbosity=2)
```

## Output Artifact Requirements

Current workflow writes/updates the following files inside `unit03/results/`.

### In `unit03/results/article_results/`

- `differentiation_test_results.csv`
- `differentiation_test_results.json`
- `differentiation_test_results.md`
- `differentiation_summary.csv`
- `differentiation_summary.json`
- `differentiation_summary.md`
- `differentiation_error_ranking.csv`
- `differentiation_freefall_coefficients.csv`
- `freefall_gravity_results.csv`
- `freefall_gravity_results.json`
- `freefall_gravity_results.md`
- `run_metadata.json`
- `unittest_report.txt`

### In `unit03/results/plots/`

For each analytic case, save:

- `<case>_error_vs_h.png`
- `<case>_error_vs_h.svg`

Examples:

- `sine_at_pi_over_4_error_vs_h.png`
- `exp_at_0p3_error_vs_h.svg`

Also save:

- `freefall_gravity_interpolation.png`
- `freefall_gravity_interpolation.svg`

### In `unit03/results/article_images/`

Save summary and analytic result tables as both `.png` and `.svg`.

Current stems include:

- `all_results_table`
- `summary_table`
- `error_ranking_table`
- `sine_at_pi_over_4_results_table`
- `exp_at_0p3_results_table`
- `poly_cubic_minus_quadratic_results_table`

Also save:

- `freefall_gravity_results_table.png`
- `freefall_gravity_results_table.svg`
- `freefall_source_data_table.png`
- `freefall_source_data_table.svg`

## Coding Conventions

Follow these conventions unless explicitly overridden:

- Use descriptive names
- Keep functions modular
- Keep the numerical method in the library file only
- Keep plotting and report generation in the script only
- Use `Path` instead of raw string paths where practical
- Use UTF-8 encoding for text outputs
- Use scientific notation for numerical reporting
- Use `matplotlib` and `numpy`
- Do not add pandas unless explicitly requested
- Do not add seaborn
- Do not add CLI argument parsing unless explicitly requested

## Execution Note

Preferred execution command in this repository:

```bash
/Users/rushisharma/Desktop/Spring 2026/5110/ECE5110/.venv/bin/python unit03/test/test_differentiation.py
```

## Exactness Requirement

When the user asks to create these files, prefer matching the established project behavior closely. If the user already provided code or a target implementation, reproduce that logic faithfully rather than inventing a new design.

## Suggested Procedure

1. Update constants in `unit03/differentiation/config.py` if case data changes.
2. Update numerical logic in `lib/differentiation_tools.py` only when method behavior changes.
3. Update aggregation/export logic in `calculators.py`, `artifacts.py`, and `visuals.py`.
4. Keep `unit03/test/test_differentiation.py` focused on assertions and workflow invocation.
5. Run the differentiation test script and verify expected artifacts exist.

## Final Checklist

- [ ] `DifferentiationTools.numerical_differentiation_3point(...)` supports central/forward/backward.
- [ ] `unit03/differentiation/workflow.py` returns rows, summary, freefall_result, dirs, and report path.
- [ ] `unit03/test/test_differentiation.py` passes all unittests.
- [ ] Differentiation CSV/JSON/Markdown/TXT outputs exist under `unit03/results/article_results/`.
- [ ] Differentiation/free-fall PNG and SVG plots exist under `unit03/results/plots/`.
- [ ] Differentiation/free-fall PNG and SVG table images exist under `unit03/results/article_images/`.
- [ ] Integration files in `unit03/results/` remain intact when differentiation workflow runs.

## Example Requests

Examples of requests that should trigger this skill:

- "Create the 3-point differentiation library and unit test script"
- "Generate lib/differentiation_tools.py and unit03/test/test_differentiation.py"
- "Update the differentiation test script so it exports article images and plots into unit03/results"
- "Add a free-fall interpolation test that estimates gravity by differentiating twice"
- "Export the gravity interpolation test into CSV/JSON/Markdown and its own plot/table images"
- "Rebuild the numerical differentiation files for Unit 03"
- "Update differentiation skill docs to match current Unit 03 outputs"
