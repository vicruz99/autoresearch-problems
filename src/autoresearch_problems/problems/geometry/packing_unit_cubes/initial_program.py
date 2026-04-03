"""Initial solution for Packing Unit Cubes: axis-aligned grid arrangement."""
import numpy as np


def solve() -> np.ndarray:
    """Pack 11 axis-aligned unit cubes in a grid arrangement."""
    # EVOLVE-BLOCK-START
    n = 11
    result = np.zeros((n, 6))
    # Arrange in a 4x3 grid (using only 11), axis-aligned (no rotation)
    cols = 4
    for i in range(n):
        row = i // cols
        col = i % cols
        result[i, 0] = col * 1.0  # cx
        result[i, 1] = row * 1.0  # cy
        result[i, 2] = 0.0        # cz
        # No rotation (rx=ry=rz=0)
    return result
    # EVOLVE-BLOCK-END
