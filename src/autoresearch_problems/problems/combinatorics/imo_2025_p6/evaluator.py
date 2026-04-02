# Adapted from google-deepmind/alphaevolve_repository_of_problems (Apache 2.0)
"""Evaluator for IMO 2025 Problem 6: Grid tiling problem.

Place non-overlapping axis-aligned rectangles on an n×n grid so that every row
and column has exactly one uncovered unit square. Minimize the number of tiles.
"""

import math
from typing import Any

import numpy as np


def _reference_tile_count(n: int) -> int:
    """A simple reference: diagonal permutation gives n*(n-1)//2 tiles."""
    # The diagonal permutation (uncovered square (i,i)) is a valid baseline.
    # Greedy tiling of the remaining cells gives at most n*(n-1)//2 tiles.
    return max(1, n * (n - 1) // 2)


def _score_tiles(tiles: list, n: int) -> tuple[float, bool, str, dict]:
    """Core scoring. Returns (score, valid, error, metrics)."""
    if not isinstance(tiles, list):
        return 0.0, False, "Output must be a list of tiles", {}
    if not tiles:
        penalty = 2 * n * (n - 1)
        return float(-1000 * penalty), False, "No tiles provided", {}

    for t in tiles:
        if not (isinstance(t, (list, tuple)) and len(t) == 4):
            return 0.0, False, f"Each tile must be (r, c, h, w), got {t!r}", {}
        r, c, h, w = t
        if not all(isinstance(x, (int, np.integer)) for x in (r, c, h, w)):
            return 0.0, False, f"Tile values must be integers, got {t!r}", {}
        if h <= 0 or w <= 0:
            return 0.0, False, f"Tile dimensions must be positive, got {t!r}", {}

    grid = np.zeros((n, n), dtype=np.int32)
    for t in tiles:
        r, c, h, w = int(t[0]), int(t[1]), int(t[2]), int(t[3])
        if r < 0 or c < 0 or r + h > n or c + w > n:
            return float(-1e9), False, f"Tile {t} out of bounds for n={n}", {}
        if np.any(grid[r: r + h, c: c + w]):
            return float(-1e9), False, f"Tile {t} overlaps another tile", {}
        grid[r: r + h, c: c + w] = 1

    uncovered_per_row = n - np.sum(grid, axis=1)
    uncovered_per_col = n - np.sum(grid, axis=0)
    row_penalty = int(np.sum(np.abs(uncovered_per_row - 1)))
    col_penalty = int(np.sum(np.abs(uncovered_per_col - 1)))
    total_penalty = row_penalty + col_penalty

    num_tiles = len(tiles)
    if total_penalty > 0:
        raw_score = float(-num_tiles - 100 * total_penalty)
        return raw_score, False, (
            f"Constraint violated: row_penalty={row_penalty}, "
            f"col_penalty={col_penalty}"
        ), {"num_tiles": num_tiles, "row_penalty": row_penalty,
             "col_penalty": col_penalty}

    ref = _reference_tile_count(n)
    score = -float(num_tiles) / float(ref)
    return score, True, "", {
        "num_tiles": num_tiles,
        "reference_tiles": ref,
        "normalized_score": score,
    }


def evaluate(output: Any, n: int = 10, **kwargs) -> dict:
    """Score a candidate tile arrangement for the n×n grid problem.

    Parameters
    ----------
    output:
        List of tiles, each a (row, col, height, width) tuple of ints.
    n:
        Grid side length.

    Returns
    -------
    dict with keys: score, valid, error, metrics.
        score: -(num_tiles / reference). Higher is better; -1.0 matches reference.
        valid: True iff all constraints satisfied.
    """
    try:
        score, valid, error, metrics = _score_tiles(output, n)
        return {"score": score, "valid": valid, "error": error, "metrics": metrics}
    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}
