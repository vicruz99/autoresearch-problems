# Adapted from google-deepmind/alphaevolve_repository_of_problems (Apache 2.0)
"""Seed solution for IMO 2025 Problem 6: grid tiling."""

import numpy as np


def _greedy_tile(n: int, uncovered_cols: list[int]) -> list[tuple]:
    """Greedily tile grid leaving column uncovered_cols[r] uncovered in row r."""
    covered = np.zeros((n, n), dtype=bool)
    for r in range(n):
        covered[r, uncovered_cols[r]] = True

    tiles = []
    for r in range(n):
        for c in range(n):
            if not covered[r, c]:
                # Extend right
                w = 0
                while c + w < n and not covered[r, c + w]:
                    w += 1
                # Extend down
                h = 1
                while r + h < n:
                    if any(covered[r + h, c + k] for k in range(w)):
                        break
                    h += 1
                tiles.append((r, c, h, w))
                for dr in range(h):
                    for dc in range(w):
                        covered[r + dr, c + dc] = True
    return tiles


def solve(n: int = 10) -> list[tuple[int, int, int, int]]:
    """Return a list of (row, col, height, width) tiles covering the n×n grid.

    Every row and column must have exactly one uncovered unit square.
    """
    # EVOLVE-BLOCK-START
    if n == 1:
        return []

    # Diagonal placement: uncovered square in row r is at column r.
    uncovered_cols = list(range(n))
    tiles = _greedy_tile(n, uncovered_cols)
    # EVOLVE-BLOCK-END
    return tiles
