---
name: unit03-workflow-infra
description: "Shared Unit 03 workflow infrastructure skill for common paths, artifact I/O, and table-image utilities used by both differentiation and integration workflows."
argument-hint: 'Task description (e.g., "update shared Unit 03 artifact utilities" or "refactor common output directory setup for differentiation and integration")'
---

# Unit 03 Workflow Infrastructure Skill

## When to Use

Use this skill for cross-cutting infrastructure that should be shared between Unit 03 numerical workflows.

Typical use cases:

- Defining shared result path constants for `unit03/results/`
- Ensuring common output folders exist (`article_results/`, `plots/`, `article_images/`)
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
  paths.py          # Shared Unit 03 path constants + directory setup helper
  artifact_io.py    # Shared CSV/JSON/Markdown/text/format helpers
  table_images.py   # Shared PNG/SVG table rendering helper
```

Domain packages should import shared helpers rather than duplicating infra code:

- `unit03/differentiation/{config,artifacts,visuals}.py`
- `unit03/integration/{config,artifacts,visuals}.py`

## Current Path Contract

- `unit03/common/paths.py` defines `PROJECT_ROOT`, `UNIT_RESULTS_DIR`, `ARTICLE_RESULTS_DIR`, `PLOTS_DIR`, `ARTICLE_IMAGES_DIR`.
- `reset_unit_results()` currently creates missing directories and returns path mappings.
- Current behavior is non-destructive: existing artifacts are preserved.

## Completion Checks

A shared-infra change is complete when:

- Both domain workflows still run and pass tests.
- Shared helpers are imported by both domains where appropriate.
- Numerical behavior and benchmark definitions remain in domain modules.
- Output artifact names and folder structure remain unchanged.
- Coexistence of differentiation and integration artifacts in `unit03/results/` is preserved unless a deliberate cleanup policy change is requested.
