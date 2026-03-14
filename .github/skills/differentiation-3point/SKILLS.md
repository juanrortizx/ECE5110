---
name: differentiation-3point
description: "Generate or update the numerical differentiation library and its unit test workflow for 3-point finite-difference methods. Use when: creating lib/differentiation_tools.py, creating scripts/test_differentiation.py, maintaining numerical differentiation utilities, generating article-ready CSV/JSON/Markdown outputs, producing error plots, and exporting table images for reports."
argument-hint: 'Task description or requested update (e.g., "create the 3-point differentiation library and test script" or "update the test script to export article images")'
---

# 3-Point Numerical Differentiation Skill

## When to Use

Use this skill when the task involves any of the following:

- Creating `lib/differentiation_tools.py`
- Creating `scripts/test_differentiation.py`
- Updating 3-point finite-difference derivative logic
- Adding or maintaining unit tests for numerical differentiation
- Generating result artifacts for reports or LaTeX articles
- Producing plots of error versus step size
- Exporting article-ready tables as `.png` and `.svg`

This skill is specifically designed for the ECE 5110 numerical methods project structure and should follow the repository conventions already in use.

## Project Context

Assume the repository follows this structure:

```text
.github/
  skills/
    ...
lib/
  differentiation_tools.py
scripts/
  test_differentiation.py
latex/
unit01_test_results/
unit02_test_results/
...
```

The generated files must fit this structure exactly:

- Library file: `lib/differentiation_tools.py`
- Test/demo/unit-test file: `scripts/test_differentiation.py`

The script should create new output folders at the project root using the naming pattern:

```text
unitXX_test_results/
```

where `XX` is the next available two-digit index.

Inside each new run folder, create:

```text
article_results/
plots/
article_images/
```

## Goal

Produce two Python files:

1. `lib/differentiation_tools.py`
2. `scripts/test_differentiation.py`

These files must work together so that the library contains the numerical method and the script:

- runs `unittest`
- evaluates several predefined test cases
- saves structured result files
- generates article-ready table images
- generates log-log error plots for each test case

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

## File 2: `scripts/test_differentiation.py`

### Purpose

This file must serve as both:

- a `unittest` test script
- a reproducible results generator for the seminar/article workflow

It should run directly as:

```python
python scripts/test_differentiation.py
```

and also support standard unittest execution.

### Import Requirements

The script should import:

```python
import csv
import json
import re
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

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
- `TEST_CASES`
- `METHODS`
- `H_VALUES`

### Required Test Cases

Include exactly these three cases unless the user explicitly requests changes:

1. `sin(x)` at `x = pi/4`
2. `exp(x)` at `x = 0.3`
3. `x^3 - 2x^2 + x - 5` at `x = 1.2`

Each case must contain:

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

## Required Functions in `scripts/test_differentiation.py`

Implement the following functions with these responsibilities.

### 1. `create_run_output_dirs(base_dir: Path)`

Must:

- scan the project root for folders matching `unit(\d+)_test_results`
- determine the next run index
- create:
  - root output folder
  - `article_results`
  - `plots`
  - `article_images`
- return all created paths plus the run index

### 2. `sanitize_filename(name: str) -> str`

Must create safe lowercase filenames by replacing non-alphanumeric characters with underscores.

### 3. `collect_results(tool: DifferentiationTools)`

Must:

- evaluate all test cases for all methods
- compute:
  - exact derivative
  - approximate derivative
  - absolute error
  - relative error
  - pass/fail against tolerance
- return a list of row dictionaries

### 4. `build_summary(rows)`

Must summarize rows by method and compute:

- number of cases
- whether all passed
- maximum absolute error
- mean absolute error
- maximum relative error
- mean relative error

### 5. `save_results(rows, article_results_dir: Path, run_index: int)`

Must save:

- `differentiation_test_results.csv`
- `differentiation_test_results.json`
- `differentiation_test_results.md`
- `differentiation_summary.csv`
- `run_metadata.json`

### 6. `format_cell(value, column_name)`

Must format table cells for image export:

- booleans as `Yes` / `No`
- floats in scientific notation
- integers as strings

### 7. `save_table_image(rows, columns, output_base: Path, title: str)`

Must:

- render a matplotlib table
- save both `.png` and `.svg`
- be suitable for article insertion

### 8. `generate_article_images(rows, article_images_dir: Path)`

Must generate these article images:

- `summary_table.png` and `.svg`
- `all_results_table.png` and `.svg`
- `error_ranking_table.png` and `.svg`

Also generate one case-specific results table per test case, using sanitized filenames.

### 9. `generate_plots(tool: DifferentiationTools, plots_dir: Path)`

Must:

- sweep over `H_VALUES`
- compute absolute error for each method
- create a log-log plot for each test case
- save each plot as both `.png` and `.svg`

## Required `unittest` Class

Create this class:

```python
class TestDifferentiationThreePoint(unittest.TestCase):
```

### `setUpClass`

In `setUpClass`, do all of the following:

- instantiate `DifferentiationTools`
- create the next output directory set
- collect result rows
- save CSV/JSON/Markdown/metadata files
- generate article images
- generate plots
- write a plain-text unit test report to:

```text
article_results/unittest_report.txt
```

### Required Tests

Implement at least these tests:

1. `test_all_methods_meet_tolerance`
   - fail with detailed messages if any method exceeds tolerance

2. `test_invalid_method_raises_value_error`
   - verify invalid method raises `ValueError`

3. `test_nonpositive_h_raises_value_error`
   - verify `h=0.0` raises `ValueError`

### Main Guard

Include:

```python
if __name__ == "__main__":
    unittest.main(verbosity=2)
```

## Output Artifact Requirements

The script must produce the following outputs inside each new `unitXX_test_results` directory.

### In `article_results/`

- `differentiation_test_results.csv`
- `differentiation_test_results.json`
- `differentiation_test_results.md`
- `differentiation_summary.csv`
- `run_metadata.json`
- `unittest_report.txt`

### In `plots/`

For each case, save:

- `<case>_error_vs_h.png`
- `<case>_error_vs_h.svg`

Examples:

- `sine_at_pi_over_4_error_vs_h.png`
- `exp_at_0p3_error_vs_h.svg`

### In `article_images/`

Save summary and result tables as both `.png` and `.svg`.

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
2. Create `scripts/test_differentiation.py`
3. Verify imports and paths are correct
4. Verify the script writes to the next available `unitXX_test_results` folder
5. Verify all required outputs are produced
6. Verify invalid input tests raise `ValueError`

## Final Checklist

Before finishing, verify all of the following:

- [ ] `lib/differentiation_tools.py` contains class `DifferentiationTools`
- [ ] `numerical_differentiation_3point` is implemented exactly with central/forward/backward 3-point formulas
- [ ] invalid `method` raises `ValueError`
- [ ] nonpositive `h` raises `ValueError`
- [ ] `scripts/test_differentiation.py` imports the library correctly
- [ ] the script defines the three required test cases
- [ ] CSV, JSON, Markdown, metadata, report, plot, and table-image outputs are generated
- [ ] output folders are created using the next available `unitXX_test_results` index
- [ ] plots are saved as both `.png` and `.svg`
- [ ] article tables are saved as both `.png` and `.svg`
- [ ] the script runs through `unittest.main(verbosity=2)`

## Example Requests

Examples of requests that should trigger this skill:

- "Create the 3-point differentiation library and unit test script"
- "Generate lib/differentiation_tools.py and scripts/test_differentiation.py"
- "Update the differentiation test script so it exports article images and plots"
- "Rebuild the numerical differentiation files for Unit 03"
