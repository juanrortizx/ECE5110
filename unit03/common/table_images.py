"""Shared table-to-image rendering helpers for Unit 03 artifacts."""

import matplotlib.pyplot as plt


def _cell_text(rows, headers):
    return [[str(row.get(header, "")) for header in headers] for row in rows]


def render_table_dual_format(rows, headers, output_stem, title=None, fontsize=9):
    """Render a table to both PNG and SVG files using the same stem path."""
    if not rows:
        rows = [{header: "" for header in headers}]

    fig, ax = plt.subplots(figsize=(max(8, len(headers) * 1.2), max(2.5, len(rows) * 0.45 + 1.8)))
    ax.axis("off")

    table = ax.table(
        cellText=_cell_text(rows, headers),
        colLabels=headers,
        loc="center",
        cellLoc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(fontsize)
    table.scale(1.0, 1.2)

    if title:
        ax.set_title(title, fontsize=11, pad=10)

    fig.tight_layout()
    fig.savefig(f"{output_stem}.png", dpi=220, bbox_inches="tight")
    fig.savefig(f"{output_stem}.svg", bbox_inches="tight")
    plt.close(fig)
