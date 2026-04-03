"""Initial solution for Sphere Packing Uncertainty: evenly spaced roots."""
import numpy as np


def solve() -> np.ndarray:
    """Return m=10 evenly spaced roots for the Laguerre combination."""
    # EVOLVE-BLOCK-START
    m = 10
    return np.linspace(38.0, 180.0, m)
    # EVOLVE-BLOCK-END
