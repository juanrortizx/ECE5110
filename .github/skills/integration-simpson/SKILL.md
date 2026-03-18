---
name: integration-simpson
description: "Generate or update the Unit 03 integration workflow with Simpson coverage, including parity validation, convergence checks, and shared integration artifact exports under unit03/results/."
argument-hint: 'Task description (e.g., "update Simpson order checks", "adjust integration outputs", or "revise integration unittest workflow")'
---

# Composite Simpson Integration Skill

## When to Use

Use this skill when the task involves:

- Creating or updating Python Simpson-integration utilities
- Implementing a composite Simpson rule API with input validation
- Building unit tests for Simpson accuracy and convergence
- Comparing Simpson and trapezoidal accuracy on shared benchmarks
- Exporting report artifacts and convergence plots

This skill follows the repository's shared integration workflow where Simpson and trapezoidal outputs are produced together.

## Layered Skill Model

Use this domain skill together with `unit03-workflow-infra` when touching shared paths/artifact I/O/table-image helpers.

- `integration-simpson`: Simpson method behavior, parity validation, convergence checks, and method-specific acceptance criteria.
- `unit03-workflow-infra`: shared path/output helpers, CSV/Markdown utilities, and shared table-image infrastructure.

## Goal

Produce or update Python files that:

1. Implement composite Simpson integration.
2. Validate correctness on analytic benchmarks.
3. Demonstrate expected fourth-order convergence on smooth problems.
4. Export report-ready outputs.

### Helper Package Layout

Shared helpers for both trapezoidal and Simpson workflows live in `unit03/integration/`:

```text
unit03/integration/
  config.py        # Paths, benchmark definitions, sweep values, expected orders
  calculators.py   # collect_method_results, observed_order, build_summary
  artifacts.py     # Directory reset, CSV/JSON/Markdown exports, report writer
  visuals.py       # Table-image utilities and error-vs-h plots
  workflow.py      # generate_all_outputs(tool) orchestration
```

Cross-domain common helpers can be centralized in:

```text
unit03/common/
  paths.py
  artifact_io.py
  table_images.py
```

`unit03/test/test_integration.py` imports `workflow.generate_all_outputs(...)` and reuses the returned rows/summaries in its assertions. Keep helper functions in their modules; do not reintroduce them into the test script.

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
composite_simpson(self, f, a, b, n)
```

Required behavior:

- Approximates $\int_a^b f(x)\,dx$ with composite Simpson's rule.
- Uses uniform spacing $h = (b-a)/n$ and requires even `n`.
- Supports callable scalar functions compatible with NumPy arrays.

Formula:

```python
h = (b - a) / n
x = np.linspace(a, b, n + 1)
y = f(x)
I = (h / 3.0) * (
    y[0]
    + y[-1]
    + 4.0 * np.sum(y[1:-1:2])
    + 2.0 * np.sum(y[2:-1:2])
)
```

Validation rules:

- Raise `ValueError` if `n <= 0`.
- Raise `ValueError` if `n` is odd.
- Raise `ValueError` if `a == b`.
- Raise `TypeError` if `f` is not callable.

Style rules:

- Keep code minimal and readable.
- Use clear NumPy-style docstrings.
- Keep plotting/export logic outside the library file.

## Test and Results Workflow

`unit03/test/test_integration.py` must:

1. Run with `python <script>` and also via unittest discovery.
2. Call `unit03.integration.workflow.generate_all_outputs(IntegrationTools())`, which:

- ensures `unit03/results/` subdirectories exist (`article_results/`, `plots/`, `article_images/`)
- collects trapezoidal and Simpson rows plus summaries
- writes all CSV/JSON/Markdown/metadata outputs for both methods
- generates error plots and article table images
- writes a joint unittest report.

3. Evaluate the benchmark set below for both methods and record absolute errors.
4. Include a parity test that confirms odd `n` is rejected for Simpson.
5. Assert that the observed log-log slopes exceed the expected 4th-order threshold.

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

- Simpson global error should scale approximately as $O(h^4)$ for smooth functions.

## Required Exports

At minimum, save the following into `unit03/results/`:

- `article_results/integration_simpson_results.{csv,json,md}`
- `article_results/integration_simpson_summary.{csv,json,md}`
- `article_results/integration_simpson_metadata.json`
- `article_results/integration_unittest_report.txt` (shared with trapezoidal summaries)
- `plots/integration_simpson_<case>_error_vs_h.{png,svg}`
- `plots/integration_simpson_error_vs_h.{png,svg}` for `x_squared`
- `article_images/integration_simpson_results_table.{png,svg}`
- `article_images/integration_simpson_summary_table.{png,svg}`

The same run also writes the trapezoidal counterparts; ensure the Simpson portion remains complete.

## Completion Checks

A Simpson workflow is complete when:

- Unit tests pass.
- All benchmark cases run and report absolute errors.
- Odd-subinterval validation is covered by tests.
- Error-vs-h plot is generated.
- Observed log-log slope is near 4 in the convergence region.
- Required outputs are written to the unit results folder.
- Existing differentiation files in `unit03/results/` remain available after an integration run.

## Common Pitfalls

- Forgetting to enforce even `n`.
- Mixing odd/even interior index sums.
- Claiming fourth-order behavior outside the asymptotic region.
- Comparing methods at unequal `n` or inconsistent benchmark definitions.

## Helper Module Responsibilities

- `config.py`: stores all benchmark definitions (`BENCHMARK_CASES`), `N_VALUES`, expected orders (4 for Simpson, 2 for trapezoidal), and path constants (`ARTICLE_RESULTS_DIR`, `PLOTS_DIR`, `ARTICLE_IMAGES_DIR`).
- `calculators.py`: implements `collect_method_results`, `observed_order`, and `build_summary`. Simpson changes should flow through these helpers rather than duplicating loops.
- `artifacts.py`: exposes `write_method_outputs(...)` and `write_unittest_report(...)`. Any new export should be added here so both methods remain consistent.
- `visuals.py`: contains `generate_article_images(...)` and `generate_error_plots(...)` using shared table/figure helpers from `unit03/common/table_images.py`.
- `workflow.py`: orchestrates the entire run via `generate_all_outputs(tool)` and returns the data that the unittest class asserts on.

`unit03/test/test_integration.py` should remain a thin unittest harness that calls `generate_all_outputs` in `setUpClass()` and then runs accuracy/order/output checks using the returned dictionaries.

## Execution Note

Preferred command in this repository:

```bash
/Users/rushisharma/Desktop/Spring 2026/5110/ECE5110/.venv/bin/python unit03/test/test_integration.py
```
