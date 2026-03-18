---
name: unit03-workflow-infra
description: "Shared Unit 03 workflow infrastructure skill for common paths, artifact I/O, and table-image utilities. Use when refactoring or maintaining cross-cutting helpers shared by differentiation and integration workflows."
argument-hint: 'Task description (e.g., "update shared Unit 03 artifact utilities" or "refactor common output directory setup for differentiation and integration")'
---

# Unit 03 Workflow Infrastructure Skill

## When to Use

Use this skill for cross-cutting infrastructure that should be shared between Unit 03 numerical workflows.

Typical use cases:

- Defining shared result path constants for `unit03/results/`
- Resetting/recreating common output folders (`article_results/`, `plots/`, `article_images/`)
- Maintaining common CSV/Markdown helper functions
- Maintaining reusable table-image rendering helpers
- Refactoring duplicated non-numerical utilities from `unit03/differentiation/` and `unit03/integration/`

## Scope Boundaries

Use this skill for shared infrastructure only, not numerical methods.

Keep numerical logic in domain skills:

- `differentiation-3point` for derivative formulas and free-fall checks
- `integration-trapezoidal` for trapezoidal method behavior and checks
- `integration-simpson` for Simpson method behavior and checks

## Recommended Shared Layout

```text
unit03/common/
  __init__.py
  paths.py          # Shared Unit 03 path constants + output directory setup
  artifact_io.py    # Shared CSV/Markdown/format helpers
  table_images.py   # Shared PNG/SVG table rendering helper
```

Domain packages should import shared helpers rather than duplicating infra code:

- `unit03/differentiation/{config,artifacts,visuals}.py`
- `unit03/integration/{config,artifacts,visuals}.py`

## Completion Checks

A shared-infra change is complete when:

- Both domain workflows still run and pass tests.
- Shared helpers are imported by both domains where appropriate.
- Numerical behavior and benchmark definitions remain in domain modules.
- Output artifact names and folder structure remain unchanged.
