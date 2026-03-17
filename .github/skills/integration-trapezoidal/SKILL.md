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

## Recommended File Targets

Use these default targets unless the user requests different locations:

- Library file: `lib/integration_tools.py`
- Test/demo file: `unit03/test/test_integration_trapezoidal.py`
- Results folder: `unit03/results/`

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

The test/demo script should:

1. Run with `python <script>` and also via unittest discovery.
2. Evaluate multiple exact-integral benchmarks.
3. Export machine-readable and article-ready outputs.
4. Plot error vs step size and verify expected slope.

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

At minimum, save:

- `integration_trapezoidal_results.csv`
- `integration_trapezoidal_results.json`
- `integration_trapezoidal_results.md`
- `integration_trapezoidal_summary.csv`
- `integration_trapezoidal_metadata.json`
- `plots/*error_vs_h*.png`

If article workflows are enabled, also export table images (`.png`, `.svg`).

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
