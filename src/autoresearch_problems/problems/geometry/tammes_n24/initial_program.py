"""Fibonacci sphere sampling for Tammes problem with n=24."""
import numpy as np


def solve() -> np.ndarray:
    """Place 24 points on the unit sphere using Fibonacci sampling."""
    # EVOLVE-BLOCK-START
    n = 24
    golden = (1 + np.sqrt(5)) / 2
    pts = []
    for i in range(n):
        theta = np.arccos(1 - 2 * (i + 0.5) / n)
        phi = 2 * np.pi * i / golden
        x = np.sin(theta) * np.cos(phi)
        y = np.sin(theta) * np.sin(phi)
        z = np.cos(theta)
        pts.append([x, y, z])
    return np.array(pts, dtype=float)
    # EVOLVE-BLOCK-END
