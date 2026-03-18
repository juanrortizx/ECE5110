"""Reusable table-image rendering for Unit 03 article artifacts."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt


def save_figure_png_svg(fig, output_stem, dpi=300, close_figure=True):
    """Save a Matplotlib figure to PNG and SVG using a shared output stem."""
    output_stem = Path(output_stem)
    output_stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_stem.with_suffix(".png"), dpi=dpi)
    fig.savefig(output_stem.with_suffix(".svg"))
    if close_figure:
        plt.close(fig)


def render_table_image(rows, columns, title, output_stem):
    """Render a table to both PNG and SVG files.

    Parameters
    ----------
    rows : list[dict]
        Table rows as dictionaries.
    columns : list[str]
        Columns to display in order.
    title : str
        Figure title.
    output_stem : pathlib.Path
        Path stem used for ``.png`` and ``.svg`` outputs.
    """
    output_stem = Path(output_stem)
    output_stem.parent.mkdir(parents=True, exist_ok=True)

    cell_text = []
    for row in rows:
        cell_text.append([str(row.get(col, "")) for col in columns])

    if not cell_text:
        cell_text = [["" for _ in columns]]

    fig_height = max(2.2, 0.5 + 0.4 * len(cell_text))
    fig, ax = plt.subplots(figsize=(max(6.5, len(columns) * 1.3), fig_height))
    ax.axis("off")
    table = ax.table(
        cellText=cell_text,
        colLabels=columns,
        loc="center",
        cellLoc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.0, 1.2)
    ax.set_title(title)
    fig.tight_layout()
    save_figure_png_svg(fig, output_stem, dpi=300, close_figure=True)
