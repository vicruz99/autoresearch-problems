"""Initial solution for Circle Packing (max sum of radii): uniform grid."""
import numpy as np


def solve() -> np.ndarray:
    """Pack 26 equal circles in a grid inside the unit square."""
    # EVOLVE-BLOCK-START
    n = 26
    cols = int(np.ceil(np.sqrt(n)))
    rows = int(np.ceil(n / cols))
    r = 0.5 / cols
    xs = np.linspace(r, 1.0 - r, cols)
    ys = np.linspace(r, 1.0 - r, rows)
    centers = np.array([[x, y] for y in ys for x in xs])[:n]
    radii = np.full(n, r)
    return np.column_stack([centers, radii])
    # EVOLVE-BLOCK-END
