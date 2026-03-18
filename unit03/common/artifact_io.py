"""Reusable artifact I/O helpers for Unit 03 workflows."""

from __future__ import annotations

import csv
import json
from pathlib import Path


def write_csv(path, rows, fieldnames):
    """Write dictionaries to CSV with a fixed field ordering."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_json(path, payload):
    """Write JSON payload with stable formatting."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def write_text(path, content):
    """Write plain text content."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def format_float(value):
    """Format numeric values for tables while keeping non-numerics unchanged."""
    if isinstance(value, float):
        return f"{value:.12g}"
    return value


def format_rows_for_columns(rows, columns, float_sigfigs=8):
    """Format row dictionaries for selected columns.

    Parameters
    ----------
    rows : list[dict]
        Row dictionaries to format.
    columns : list[str]
        Column names to extract and preserve order.
    float_sigfigs : int, optional
        Significant figures for floating-point formatting.
    """
    fmt = f"{{:.{int(float_sigfigs)}g}}"
    formatted = []
    for row in rows:
        formatted.append(
            {
                key: (fmt.format(row.get(key)) if isinstance(row.get(key), float) else row.get(key))
                for key in columns
            }
        )
    return formatted


def markdown_table(rows, headers):
    """Render a GitHub-flavored Markdown table from dictionaries."""
    header_line = "| " + " | ".join(headers) + " |"
    separator = "| " + " | ".join(["---"] * len(headers)) + " |"
    body = []
    for row in rows:
        values = [str(format_float(row.get(col, ""))) for col in headers]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header_line, separator] + body)


def markdown_table_formatted(rows, headers, float_sigfigs=8):
    """Render Markdown table with caller-configurable float precision."""
    formatted_rows = format_rows_for_columns(rows, headers, float_sigfigs=float_sigfigs)
    return markdown_table(formatted_rows, headers)
