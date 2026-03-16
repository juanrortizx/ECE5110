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

## Recommended File Targets

Use these default targets unless the user requests different locations:

- Library file: `lib/integration_tools.py`
- Test/demo file: `unit03/test/test_integration_simpson.py`
- Results folder: `unit03/results/`

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

The test/demo script should:

1. Run with `python <script>` and also via unittest discovery.
2. Evaluate exact-integral benchmarks and report per-case errors.
3. Include a parity test that confirms odd `n` is rejected.
4. Export machine-readable and article-ready outputs.

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

At minimum, save:

- `integration_simpson_results.csv`
- `integration_simpson_results.json`
- `integration_simpson_results.md`
- `integration_simpson_summary.csv`
- `integration_simpson_metadata.json`
- `plots/*error_vs_h*.png`

If article workflows are enabled, also export table images (`.png`, `.svg`).

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
