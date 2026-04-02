"""Initial solution for the Ovals problem: a circle with constant phi."""
import numpy as np


def solve():
    """Return [x, y, phi] control points for a unit circle with phi=1."""
    # EVOLVE-BLOCK-START
    n = 100
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    x = np.cos(t)
    y = np.sin(t)
    phi = np.ones(n)
    return [x, y, phi]
    # EVOLVE-BLOCK-END
