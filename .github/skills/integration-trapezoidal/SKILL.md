---
name: integration-trapezoidal
description: "Generate or update Python numerical integration workflows using the composite trapezoidal rule. Use when: creating integration utilities, building trapezoidal unit tests, exporting error tables/plots, and validating convergence against known analytic integrals."
argument-hint: 'Task description or requested update (e.g., "create trapezoidal integration library and tests" or "add convergence plots and report exports for the trapezoidal rule")'
---

# Composite Trapezoidal Integration Skill

## When to Use

Use this skill when the task involves any of the following:

- Creating or updating Python trapezoidal-integration utilities
- Implementing a reusable composite trapezoidal rule API
- Creating integration-focused unit tests and reproducible scripts
- Validating numerical integration against known exact integrals
- Exporting CSV, JSON, and Markdown result artifacts for reports
- Generating error-versus-step-size plots to verify convergence

This skill is designed for numerical methods workflows in this repository and should follow existing project conventions.

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
  artifacts.py     # Directory clearing, CSV/JSON/Markdown exporters, report writer
  visuals.py       # Table images and error-vs-h plots
  workflow.py      # generate_all_outputs(tool) orchestrator
```

`unit03/test/test_integration.py` remains a single unittest harness that calls `workflow.generate_all_outputs(...)` and then runs assertions specific to each method.

## Recommended File Targets

Use these default targets unless the user requests different locations:

- Library file: `lib/integration_tools.py`
- Helper package: `unit03/integration/` (`config.py`, `calculators.py`, `artifacts.py`, `visuals.py`, `workflow.py`)
- Test/demo file: `unit03/test/test_integration.py`
- Results folder: `unit03/results/` (clear + recreate on each run)

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
2. Invoke `unit03.integration.workflow.generate_all_outputs(IntegrationTools())`, which resets `unit03/results/`, computes both trapezoidal and Simpson rows, writes every CSV/JSON/Markdown file, generates plots/table images, and emits a unified unittest report.
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

At minimum, a run that exercises the trapezoidal method must emit:

- `article_results/integration_trapezoidal_results.{csv,json,md}`
- `article_results/integration_trapezoidal_summary.csv`
- `article_results/integration_trapezoidal_metadata.json`
- `article_results/integration_unittest_report.txt` (shared summary)
- `plots/integration_trapezoidal_<case>_error_vs_h.{png,svg}`
- `article_images/integration_trapezoidal_results_table.{png,svg}`
- `article_images/integration_trapezoidal_summary_table.{png,svg}`

The same execution also produces the Simpson outputs; confirm that both sets appear after the `unit03/results/` reset.

## Completion Checks

A trapezoidal workflow is complete when:

- Unit tests pass.
- All benchmark cases run and report absolute errors.
- Error-vs-h plot is generated.
- Observed log-log slope is near 2 in the convergence region.
- Required output artifacts are written to the unit results folder.

## Common Pitfalls

- Forgetting endpoint half-weights in the trapezoidal sum.
- Using too few $n$ values to show a clear slope region.
- Mixing scalar and vector function assumptions without handling NumPy input.
- Interpreting very-small-$h$ floating-point effects as method failure.

## Helper Module Responsibilities

- `config.py` centralizes benchmark data, `N_VALUES`, expected orders, and output paths so both methods share identical inputs.
- `calculators.py` gathers per-method rows and computes observed convergence orders; extend these helpers instead of duplicating loops.
- `artifacts.py` is responsible for clearing `unit03/results/`, exporting every CSV/JSON/Markdown file, and writing the unified unittest report.
- `visuals.py` renders the PNG/SVG table images and the log-log error plots for each benchmark.
- `workflow.py` ties everything together via `generate_all_outputs(tool)` and returns dictionaries consumed by `unit03/test/test_integration.py`.

Any update to trapezoidal behavior should pass through these helpers so Simpson automatically benefits from shared improvements.
