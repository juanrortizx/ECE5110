---
name: integration-simpson
description: "Generate or update Python numerical integration workflows using composite Simpson's rule. Use when: creating Simpson integration utilities, building even-subinterval validation tests, exporting error tables/plots, and confirming fourth-order convergence on smooth integrands."
argument-hint: 'Task description or requested update (e.g., "create Simpson integration library and tests" or "add Simpson convergence validation and report exports")'
---

# Composite Simpson Integration Skill

## When to Use

Use this skill when the task involves any of the following:

- Creating or updating Python Simpson-integration utilities
- Implementing a composite Simpson rule API with input validation
- Building unit tests for Simpson accuracy and convergence
- Comparing Simpson and trapezoidal accuracy on shared benchmarks
- Exporting report artifacts and convergence plots

This skill is designed for numerical methods workflows in this repository and should follow existing project conventions.

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

`unit03/test/test_integration.py` imports `workflow.generate_all_outputs(...)` and reuses the returned rows/summaries in its assertions. Keep helper functions in their modules; do not reintroduce them into the test script.

## Recommended File Targets

Use these default targets unless the user requests different locations:

- Library file: `lib/integration_tools.py`
- Helper package: `unit03/integration/` (`config.py`, `calculators.py`, `artifacts.py`, `visuals.py`, `workflow.py`)
- Test/demo file: `unit03/test/test_integration.py`
- Results folder: `unit03/results/` (cleared and recreated each run)

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
   - clears and recreates `unit03/results/` (`article_results/`, `plots/`, `article_images/`)
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

At minimum, save the following into `unit03/results/` (after clearing it at the start of the run):

- `article_results/integration_simpson_results.{csv,json,md}`
- `article_results/integration_simpson_summary.csv`
- `article_results/integration_simpson_metadata.json`
- `article_results/integration_unittest_report.txt` (shared with trapezoidal summaries)
- `plots/integration_simpson_<case>_error_vs_h.{png,svg}`
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

## Common Pitfalls

- Forgetting to enforce even `n`.
- Mixing odd/even interior index sums.
- Claiming fourth-order behavior outside the asymptotic region.
- Comparing methods at unequal `n` or inconsistent benchmark definitions.

## Helper Module Responsibilities

- `config.py`: stores all benchmark definitions (`BENCHMARK_CASES`), `N_VALUES`, expected orders (4 for Simpson, 2 for trapezoidal), and path constants (`ARTICLE_RESULTS_DIR`, `PLOTS_DIR`, `ARTICLE_IMAGES_DIR`).
- `calculators.py`: implements `collect_method_results`, `observed_order`, and `build_summary`. Simpson changes should flow through these helpers rather than duplicating loops.
- `artifacts.py`: exposes `prepare_output_dirs()` (which clears/rebuilds the result tree), `write_method_outputs(...)`, and `write_unittest_report(...)`. Any new artifact goes here so both methods benefit.
- `visuals.py`: contains `generate_article_images(...)` and `generate_error_plots(...)` plus the shared `save_table_image(...)`.
- `workflow.py`: orchestrates the entire run via `generate_all_outputs(tool)` and returns the data that the unittest class asserts on.

`unit03/test/test_integration.py` should remain a thin unittest harness that calls `generate_all_outputs` in `setUpClass()` and then runs accuracy/order/output checks using the returned dictionaries.
