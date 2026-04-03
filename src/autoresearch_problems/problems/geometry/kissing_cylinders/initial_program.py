"""Initial configuration for the Kissing Cylinders problem."""
import numpy as np


def solve() -> np.ndarray:
    """
    Return 7 cylinders arranged symmetrically around the Z-axis at axis-to-axis
    distance 2, each cylinder tilted at 45 degrees.
    """
    # EVOLVE-BLOCK-START
    n = 7
    result = np.zeros((n, 6))
    for i in range(n):
        angle = 2 * np.pi * i / n
        # Position in XY plane at distance 2
        px = 2.0 * np.cos(angle)
        py = 2.0 * np.sin(angle)
        pz = 0.0
        # Direction: slightly tilted from XY plane
        vx = np.cos(angle + np.pi / 2) * np.sin(np.pi / 4)
        vy = np.sin(angle + np.pi / 2) * np.sin(np.pi / 4)
        vz = np.cos(np.pi / 4)
        result[i] = [px, py, pz, vx, vy, vz]
    return result
    # EVOLVE-BLOCK-END
