# Adapted from google-deepmind/alphaevolve_repository_of_problems (Apache 2.0)
"""Initial program for the 2D Kakeya needle problem."""

import time
import numpy as np


def get_score(x: np.ndarray) -> float:
    """Compute negative union area (higher is better)."""
    try:
        from shapely import geometry
        n = len(x)
        delta = 1.0 / n
        polygons = []
        for i in range(1, n + 1):
            ai = i / n
            xi = float(x[i - 1])
            polygons.append(geometry.Polygon([(xi, 0), (xi + delta, 0), (xi + ai, 1)]))
        union = polygons[0]
        for p in polygons[1:]:
            union = union.union(p)
        return -union.area
    except Exception:
        return -1e9


def solve(n: int = 32) -> np.ndarray:
    """Return positions x = [x_1, ..., x_n] minimising the union area.

    # EVOLVE-BLOCK-START
    """
    best_positions = np.linspace(0, 1, n)
    best_score = get_score(best_positions)
    curr_positions = best_positions.copy()

    start_time = time.time()
    while time.time() - start_time < 100:
        random_index = np.random.randint(0, len(curr_positions))
        curr_positions = best_positions.copy()
        curr_positions[random_index:] += 1e-1 * np.random.uniform(-1, 1)
        curr_score = get_score(curr_positions)
        if curr_score > best_score:
            best_score = curr_score
            best_positions = curr_positions.copy()

    return best_positions
    # EVOLVE-BLOCK-END


if __name__ == "__main__":
    result = solve(n=32)
    print("Positions:", result)
    print("Score:", get_score(result))
