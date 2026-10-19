from __future__ import annotations

import math
from collections.abc import Sequence
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

from .runs import Run, ScriptClass

_DEFAULT_COLORS = [
    "#b8b8b8",  # numeric
    "#c43c39",  # Cyrillic
    "#3974b8",  # Latin
    "#6f6f6f",  # other
]


def log_radius(length: int, base: float = 10.0) -> int:
    if length < 1:
        raise ValueError("length must be at least 1")
    if base <= 1:
        raise ValueError("base must be greater than 1")
    return max(0, math.floor(math.log(length, base) + 0.5))


def runs_to_pixels(
    runs: Sequence[Run],
    *,
    base: float = 10.0,
) -> np.ndarray:
    """Convert one-run-per-column data into a centered pixel matrix."""
    if not runs:
        return np.empty((0, 0), dtype=float)

    radii = [log_radius(run.length, base) for run in runs]
    maximum = max(radii)
    height = 2 * maximum + 1
    center = maximum
    pixels = np.full((height, len(runs)), np.nan)

    for column, (run, radius) in enumerate(zip(runs, radii)):
        pixels[
            center - radius : center + radius + 1,
            column,
        ] = int(run.script)

    return pixels


def plot_runs(
    runs: Sequence[Run],
    output_path: str | Path | None = None,
    *,
    base: float = 10.0,
    title: str | None = None,
    radius_limit: int | None = None,
):
    """Plot one maximal script run per column."""
    pixels = runs_to_pixels(runs, base=base)
    figure, axis = plt.subplots(figsize=(14, 4))

    masked = np.ma.masked_invalid(pixels)
    axis.imshow(
        masked,
        aspect="auto",
        interpolation="nearest",
        cmap=ListedColormap(_DEFAULT_COLORS),
        vmin=0,
        vmax=3,
    )
    if radius_limit is not None:
        local_radius = (pixels.shape[0] - 1) // 2
        if radius_limit < local_radius:
            raise ValueError("radius_limit must cover all plotted runs")
        axis.set_ylim(local_radius + radius_limit + 0.5,
                      local_radius - radius_limit - 0.5)
    axis.set_xlabel("Script-run index (cumulative script-class changes, from 0)")
    axis.set_ylabel("Rounded logarithmic radius")
    axis.set_yticks([])
    axis.set_title(
        title
        or f"War and Peace language runs (logarithm base {base:g})"
    )

    legend_handles = [
        plt.Line2D(
            [0],
            [0],
            marker="s",
            linestyle="",
            markerfacecolor=color,
            markeredgecolor=color,
            label=label,
        )
        for color, label in zip(
            _DEFAULT_COLORS,
            ["Numeric", "Cyrillic", "Latin", "Other"],
        )
    ]
    axis.legend(
        handles=legend_handles,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.18),
        ncol=4,
        frameon=False,
    )
    figure.tight_layout()

    if output_path is not None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(path, dpi=180, bbox_inches="tight")

    return figure, axis
