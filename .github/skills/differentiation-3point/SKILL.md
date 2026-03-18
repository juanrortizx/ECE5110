---
name: differentiation-3point
description: "Generate or update the numerical differentiation library and its unit test workflow for 3-point finite-difference methods. Use when: creating lib/differentiation_tools.py, creating unit03/test/test_differentiation.py, maintaining numerical differentiation utilities, generating article-ready CSV/JSON/Markdown outputs, producing error plots, exporting table images for reports, and validating a free-fall gravity estimate from interpolated data."
argument-hint: 'Task description or requested update (e.g., "create the 3-point differentiation library and unit03/test/test_differentiation.py" or "update the unit test script to export article images and add the gravity interpolation test")'
---

# 3-Point Numerical Differentiation Skill

## When to Use

Use this skill when the task involves any of the following:

- Creating `lib/differentiation_tools.py`
- Creating `unit03/test/test_differentiation.py`
- Updating 3-point finite-difference derivative logic
- Adding or maintaining unit tests for numerical differentiation
- Generating result artifacts for reports or LaTeX articles
- Producing plots of error versus step size
- Exporting article-ready tables as `.png` and `.svg`
- Validating gravitational acceleration from interpolated free-fall data by differentiating twice
- Exporting the gravity validation into dedicated CSV, JSON, Markdown, plot, and table-image outputs

This skill is specifically designed for the ECE 5110 numerical methods project structure and should follow the repository conventions already in use.

## Layered Skill Model

Use this domain skill together with `unit03-workflow-infra` when changes involve shared infrastructure.

- `differentiation-3point`: numerical differentiation behavior, tolerances, free-fall validation, and differentiation-specific outputs.
- `unit03-workflow-infra`: shared path setup, artifact I/O helpers, and common table-image rendering used by multiple Unit 03 domains.

### Helper Package Layout

Differentiation logic is modularized under `unit03/differentiation/`:

```text
unit03/differentiation/
  config.py          # Paths, constants, analytic test cases, free-fall data
  calculators.py     # Numerical result collection + gravity estimation helpers
  artifacts.py       # Directory reset, markdown writers, CSV/JSON exports, report writer
  visuals.py         # Table-image generation and matplotlib plots
  workflow.py        # `generate_all_outputs(tool)` orchestration entry point
```

Shared cross-domain helpers may live in:

```text
unit03/common/
  paths.py
  artifact_io.py
  table_images.py
```

`unit03/test/test_differentiation.py` should import `generate_all_outputs` and the needed constants instead of redefining helpers inline. When updating this workflow, edit the module that owns the relevant responsibility (constants in `config.py`, filesystem work in `artifacts.py`, etc.) so future runs stay modular.

## Project Context

Assume the repository follows this structure:

```text
.github/
  skills/
    ...
lib/
  differentiation_tools.py
unit03/
  test/
    test_differentiation.py
  results/
latex/
```

The generated files must fit this structure exactly:

- Library file: `lib/differentiation_tools.py`
- Test/demo/unit-test file: `unit03/test/test_differentiation.py`

The script should store outputs in the existing Unit 03 results folder:

```text
unit03/results/
```

Before each run, the script should clear and replace the previous contents of `unit03/results/`.

Inside `unit03/results/`, create:

```text
article_results/
plots/
article_images/
```

## Goal

Produce:

1. `lib/differentiation_tools.py`
2. the helper modules listed above in `unit03/differentiation/`
3. `unit03/test/test_differentiation.py`, which orchestrates the helpers

These files must work together so that the library contains the numerical method, the helper modules handle reporting/plotting/output duties, and the script:

- runs `unittest`
- evaluates several predefined analytic test cases
- validates a free-fall gravity estimate from interpolated data
- saves structured result files
- generates article-ready table images
- generates log-log error plots for each analytic test case
- generates dedicated free-fall export files and visuals

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

Implement exactly this public method:

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

- Keep the implementation minimal and readable
- Use clear docstrings in NumPy style
- Do not include plotting code in this file
- Do not add unrelated methods unless explicitly requested

## File 2: `unit03/test/test_differentiation.py`

### Purpose

This file must serve as both:

- a `unittest` test script
- a reproducible results generator for the seminar/article workflow

It should run directly as:

```python
python unit03/test/test_differentiation.py
```

and also support standard unittest execution.

### Import Requirements

The script should import:

```python
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
```

It must also add the project root to `sys.path` so it can import:

```python
from lib.differentiation_tools import DifferentiationTools
```

### Required Constants

Define:

- `SCRIPT_DIR`
- `PROJECT_ROOT`
- `UNIT_RESULTS_DIR`
- `TEST_CASES`
- `METHODS`
- `H_VALUES`
- `FREEFALL_POSITION_DATA`
- `FREEFALL_TIME_DATA`
- `FREEFALL_GRAVITY_TOL`

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

- Defines project/root paths, `UNIT_RESULTS_DIR`, and the required subdirectories.
- Declares `TEST_CASES`, `METHODS`, `H_VALUES`, `FREEFALL_POSITION_DATA`, `FREEFALL_TIME_DATA`, and `FREEFALL_GRAVITY_TOL`.
- Any change to analytic cases or constants must be reflected here so every helper uses the same data.

### `unit03/differentiation/calculators.py`

- `build_freefall_position_interpolant()` creates the quadratic interpolant from the free-fall arrays.
- `estimate_gravity_from_interpolated_freefall(tool, h)` differentiates the interpolant twice (central method, same `h`) and returns the metadata dictionary (step size, signed/magnitude estimate, tolerances, source arrays, coefficients).
- `collect_results(tool)` evaluates each analytic test case for every method, capturing exact/approximate derivatives plus absolute/relative errors and pass/fail flags.
- `build_summary(rows)` collapses rows per method and reports counts plus max/mean absolute/relative error values.

### `unit03/differentiation/artifacts.py`

- `create_output_dirs()` clears `unit03/results/` and recreates `article_results/`, `plots/`, and `article_images/`.
- `sanitize_filename()` normalizes case-specific filenames; `format_cell()` unifies table formatting.
- `_markdown_table()` (internal) plus `save_results(rows, freefall_result)` write all CSV/JSON/Markdown/metadata files listed in the Output Artifact Requirements, including the detailed free-fall Markdown content.
- `write_unittest_report(rows, freefall_result)` exports the plain-text summary (analytic + gravity sections) into `article_results/unittest_report.txt`.

### `unit03/differentiation/visuals.py`

- `save_table_image(...)` renders PNG/SVG table images.
- `generate_article_images(rows, article_images_dir, freefall_result)` produces the summary/all-results/error-ranking tables, per-case tables, and the two free-fall tables.
- `generate_plots(tool, plots_dir, freefall_result)` sweeps `H_VALUES` for each analytic case (log-log PNG/SVG) and produces the dedicated free-fall interpolation plot that overlays the data, interpolant, evaluation point, and estimated |g|.

### `unit03/differentiation/workflow.py`

- Exposes `generate_all_outputs(tool)` which:
  - calls `create_output_dirs()`
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
- create the Unit 03 output directory set inside `unit03/results`
- clear any previous generated results in that folder before writing new ones
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

### Required Tests

Implement at least these tests:

1. `test_all_methods_meet_tolerance`
   - fail with detailed messages if any analytic method exceeds tolerance

2. `test_gravity_from_interpolated_freefall_data`
   - use the stored free-fall gravity estimate
   - verify `abs(accel_est)` is within `FREEFALL_GRAVITY_TOL` of `9.81`

3. `test_invalid_method_raises_value_error`
   - verify invalid method raises `ValueError`

4. `test_nonpositive_h_raises_value_error`
   - verify `h=0.0` raises `ValueError`

### Main Guard

Include:

```python
if __name__ == "__main__":
    unittest.main(verbosity=2)
```

## Output Artifact Requirements

The script must produce the following outputs inside `unit03/results/`.

### In `unit03/results/article_results/`

- `differentiation_test_results.csv`
- `differentiation_test_results.json`
- `differentiation_test_results.md`
- `differentiation_summary.csv`
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

## Exactness Requirement

When the user asks to create these files, prefer matching the established project behavior closely. If the user already provided code or a target implementation, reproduce that logic faithfully rather than inventing a new design.

## Suggested Generation Procedure

When using this skill to generate the files, follow this order:

1. Create `lib/differentiation_tools.py`
2. Create `unit03/test/test_differentiation.py`
3. Verify imports and paths are correct
4. Verify the script writes to `unit03/results`
5. Verify the folder is cleared and regenerated on each run
6. Verify all required outputs are produced
7. Verify invalid input tests raise `ValueError`
8. Verify the free-fall gravity check estimates an acceleration magnitude close to `9.81 m/s^2`
9. Verify the dedicated free-fall CSV, JSON, Markdown, plot, and table-image outputs are generated

## Final Checklist

Before finishing, verify all of the following:

- [ ] `lib/differentiation_tools.py` contains class `DifferentiationTools`
- [ ] `numerical_differentiation_3point` is implemented exactly with central/forward/backward 3-point formulas
- [ ] invalid `method` raises `ValueError`
- [ ] nonpositive `h` raises `ValueError`
- [ ] `unit03/test/test_differentiation.py` imports the library correctly
- [ ] the script defines the three required analytic test cases
- [ ] the script defines the required free-fall position and time arrays and gravity tolerance constant
- [ ] the script includes a quadratic interpolant helper for the free-fall data
- [ ] the script includes a gravity-estimation unit test based on differentiating the interpolant twice
- [ ] analytic CSV, JSON, Markdown, metadata, report, plot, and table-image outputs are generated
- [ ] dedicated free-fall CSV, JSON, Markdown, plot, and table-image outputs are generated
- [ ] outputs are written to `unit03/results`
- [ ] previous generated contents in `unit03/results` are cleared before each run
- [ ] plots are saved as both `.png` and `.svg`
- [ ] article tables are saved as both `.png` and `.svg`
- [ ] the gravity test checks acceleration magnitude against `9.81` with an appropriate tolerance
- [ ] the script runs through `unittest.main(verbosity=2)`

## Example Requests

Examples of requests that should trigger this skill:

- "Create the 3-point differentiation library and unit test script"
- "Generate lib/differentiation_tools.py and unit03/test/test_differentiation.py"
- "Update the differentiation test script so it exports article images and plots into unit03/results"
- "Add a free-fall interpolation test that estimates gravity by differentiating twice"
- "Export the gravity interpolation test into CSV/JSON/Markdown and its own plot/table images"
- "Rebuild the numerical differentiation files for Unit 03"
