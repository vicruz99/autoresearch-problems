"""Seed solution for the Equidistant Points in Convex Polygons problem."""

import math

import numpy as np


def solve(num_vertex: int = 10) -> np.ndarray:
    """Return a regular polygon as a baseline convex polygon.

    A regular polygon places all vertices on a circle, so the distances from
    any vertex v to the rest take exactly floor(num_vertex / 2) distinct values,
    each occurring at most twice.  This scores poorly (no 4 equidistant
    neighbours from any vertex) but is a valid convex polygon and a correct
    baseline.
    """
    # EVOLVE-BLOCK-START
    angles = np.linspace(0, 2 * math.pi, num_vertex, endpoint=False)
    vertices = np.column_stack([np.cos(angles), np.sin(angles)])
    # EVOLVE-BLOCK-END
    return vertices
