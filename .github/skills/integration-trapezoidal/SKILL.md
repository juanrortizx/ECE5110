---
name: integration-trapezoidal
description: "Generate or update the Unit 03 integration workflow with trapezoidal coverage, including shared trapezoidal/Simpson outputs, convergence checks, and artifact exports under unit03/results/."
argument-hint: 'Task description (e.g., "adjust trapezoidal convergence thresholds", "update integration exports", or "modify integration unittest workflow")'
---

# Composite Trapezoidal Integration Skill

## When to Use

Use this skill when the task involves:

- Creating or updating Python trapezoidal-integration utilities
- Implementing a reusable composite trapezoidal rule API
- Creating integration-focused unit tests and reproducible scripts
- Validating numerical integration against known exact integrals
- Exporting CSV, JSON, and Markdown result artifacts for reports
- Generating error-versus-step-size plots to verify convergence

This skill follows the current shared integration workflow where trapezoidal and Simpson outputs are generated together.

## Layered Skill Model

Use this domain skill together with `unit03-workflow-infra` when a change touches shared paths/artifact I/O/table-image helpers.

- `integration-trapezoidal`: trapezoidal method behavior, validation, convergence checks, and method-specific assertions.
- `unit03-workflow-infra`: shared path constants, output-directory setup, artifact I/O helpers, and reusable table-image utilities.

## Goal

Produce or update Python files that:

1. Implement composite trapezoidal integration.
2. Validate correctness using analytic test integrals.
3. Demonstrate expected convergence behavior.
4. Export report-ready artifacts.

### Helper Package Layout

Both trapezoidal and Simpson workflows reuse the `unit03/integration/` helper package:

```text
unit03/integration/
  config.py        # Paths, benchmark cases, sweep sizes, target orders
  calculators.py   # collect_method_results, observed_order, build_summary
  artifacts.py     # CSV/JSON/Markdown exporters, metadata + report writer
  visuals.py       # Table images and error-vs-h plots
  workflow.py      # generate_all_outputs(tool) orchestrator
```

Cross-domain utilities may live under:

```text
unit03/common/
  paths.py
  artifact_io.py
  table_images.py
```

`unit03/test/test_integration.py` remains a single unittest harness that calls `workflow.generate_all_outputs(...)` and then runs assertions specific to each method.

## Current File Targets

Use these default targets unless the user requests different locations:

- Library file: `lib/integration_tools.py`
- Helper package: `unit03/integration/` (`config.py`, `calculators.py`, `artifacts.py`, `visuals.py`, `workflow.py`)
- Test/demo file: `unit03/test/test_integration.py`
- Results folder: `unit03/results/` (directories created if missing)

If the user specifies another unit folder, keep the same structure under that unit.

## Library Requirements

Create or update a class named:

```python
IntegrationTools
```

Implement at least this public method:

```python
composite_trapezoidal(self, f, a, b, n)
```

Required behavior:

- Approximates $\int_a^b f(x)\,dx$ with the composite trapezoidal rule.
- Uses uniform spacing $h = (b-a)/n$.
- Supports callable scalar functions compatible with NumPy arrays.

Formula:

```python
h = (b - a) / n
x = np.linspace(a, b, n + 1)
y = f(x)
I = h * (0.5 * y[0] + np.sum(y[1:-1]) + 0.5 * y[-1])
```

Validation rules:

- Raise `ValueError` if `n <= 0`.
- Raise `ValueError` if `a == b`.
- Raise `TypeError` if `f` is not callable.

Style rules:

- Keep code minimal and readable.
- Use clear NumPy-style docstrings.
- Keep plotting/export logic outside the library file.

## Test and Results Workflow

`unit03/test/test_integration.py` must:

1. Run with `python <script>` and also via unittest discovery.
2. Invoke `unit03.integration.workflow.generate_all_outputs(IntegrationTools())`, which:

- ensures output directories exist via `unit03.common.paths.reset_unit_results()`
- computes both trapezoidal and Simpson rows
- writes per-method CSV/JSON/Markdown/metadata outputs
- generates per-method table images and error plots
- writes `integration_unittest_report.txt`

3. Evaluate the benchmark set below for both methods (shared `BENCHMARK_CASES` from `config.py`).
4. Ensure trapezoidal validation covers callable checks, positive `n`, and nonzero interval width.
5. Assert that observed log-log slopes hover near the $O(h^2)$ expectation.

Recommended benchmark set:

1. $\int_0^1 x^2\,dx = 1/3$
2. $\int_0^{\pi} \sin(x)\,dx = 2$
3. $\int_0^1 e^x\,dx = e-1$
4. $\int_0^1 \frac{4}{1+x^2}\,dx = \pi$

Use subinterval sweeps such as:

```python
N_VALUES = [4, 8, 16, 32, 64, 128, 256]
```

Expected convergence:

- Trapezoidal global error should scale approximately as $O(h^2)$ for smooth functions.

## Required Exports

A complete run currently emits trapezoidal files:

- `article_results/integration_trapezoidal_results.{csv,json,md}`
- `article_results/integration_trapezoidal_summary.{csv,json,md}`
- `article_results/integration_trapezoidal_metadata.json`
- `article_results/integration_unittest_report.txt` (shared summary)
- `plots/integration_trapezoidal_<case>_error_vs_h.{png,svg}`
- `plots/integration_trapezoidal_error_vs_h.{png,svg}` for `x_squared`
- `article_images/integration_trapezoidal_results_table.{png,svg}`
- `article_images/integration_trapezoidal_summary_table.{png,svg}`

The same execution also writes the Simpson counterparts in the same run.

## Completion Checks

A trapezoidal workflow is complete when:

- Unit tests pass.
- All benchmark cases run and report absolute errors.
- Error-vs-h plot is generated.
- Observed log-log slope is near 2 in the convergence region.
- Required output artifacts are written to the unit results folder.
- Existing differentiation artifacts in `unit03/results/` are not removed by this workflow.

## Common Pitfalls

- Forgetting endpoint half-weights in the trapezoidal sum.
- Using too few $n$ values to show a clear slope region.
- Mixing scalar and vector function assumptions without handling NumPy input.
- Interpreting very-small-$h$ floating-point effects as method failure.

## Helper Module Responsibilities

- `config.py` centralizes benchmark data, `N_VALUES`, expected orders, and output paths so both methods share identical inputs.
- `calculators.py` gathers per-method rows and computes observed convergence orders; extend these helpers instead of duplicating loops.
- `artifacts.py` exports every CSV/JSON/Markdown file plus metadata, and writes the unified unittest report.
- `visuals.py` renders the PNG/SVG table images and the log-log error plots for each benchmark.
- `workflow.py` ties everything together via `generate_all_outputs(tool)` and returns dictionaries consumed by `unit03/test/test_integration.py`.

Any update to trapezoidal behavior should pass through these helpers so Simpson automatically benefits from shared improvements.

## Execution Note

Preferred command in this repository:

```bash
/Users/rushisharma/Desktop/Spring 2026/5110/ECE5110/.venv/bin/python unit03/test/test_integration.py
```
