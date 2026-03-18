"""Shared artifact writers for Unit 03 workflows."""

import csv
import json
from pathlib import Path


def as_path(path_value):
    return path_value if isinstance(path_value, Path) else Path(path_value)


def format_sci(value):
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return f"{value:.8e}"
    return str(value)


def write_csv(rows, headers, output_path):
    output_path = as_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as file_handle:
        writer = csv.DictWriter(file_handle, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key) for key in headers})


def write_json(payload, output_path):
    output_path = as_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file_handle:
        json.dump(payload, file_handle, indent=2, ensure_ascii=True)


def write_markdown_table(rows, headers, output_path):
    output_path = as_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

    for row in rows:
        values = [format_sci(row.get(header)) for header in headers]
        lines.append("| " + " | ".join(values) + " |")

    with output_path.open("w", encoding="utf-8") as file_handle:
        file_handle.write("\n".join(lines) + "\n")


def write_text(text, output_path):
    output_path = as_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file_handle:
        file_handle.write(text)
