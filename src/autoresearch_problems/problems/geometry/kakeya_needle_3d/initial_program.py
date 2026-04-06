# Adapted from google-deepmind/alphaevolve_repository_of_problems (Apache 2.0)
"""Initial program for the 3D Kakeya needle problem."""

import time
import numpy as np


def get_score(positions) -> float:
    """Estimate negative union volume of tubes (higher is better)."""
    x_pos, y_pos = positions[0], positions[1]
    n = int(round(np.sqrt(len(x_pos))))
    inv_n = 1.0 / n

    rng = np.random.default_rng(42)
    num_samples = 50_000
    extent = 1.0 + inv_n
    pts = rng.uniform(0, 1, size=(num_samples, 3))
    pts[:, 0] *= extent
    pts[:, 1] *= extent
    a, b, c = pts[:, 0], pts[:, 1], pts[:, 2]

    in_union = np.zeros(num_samples, dtype=bool)
    for idx in range(n * n):
        xi, yi = float(x_pos[idx]), float(y_pos[idx])
        ii, ji = idx // n, idx % n
        x_min = (1 - c) * xi + c * (xi + ii * inv_n)
        x_max = (1 - c) * (xi + inv_n) + c * (xi + (ii + 1) * inv_n)
        y_min = (1 - c) * yi + c * (yi + ji * inv_n)
        y_max = (1 - c) * (yi + inv_n) + c * (yi + (ji + 1) * inv_n)
        in_union |= (x_min <= a) & (a <= x_max) & (y_min <= b) & (b <= y_max)

    return -float(np.mean(in_union)) * extent * extent


def solve(cap_n: int = 8, **kwargs):
    """Return positions minimising the 3D union volume.

    # EVOLVE-BLOCK-START
    """
    n = int(cap_n)
    num_tubes = n * n
    best_x = np.random.uniform(0, 1, size=num_tubes)
    best_y = np.random.uniform(0, 1, size=num_tubes)
    best_positions = [best_x, best_y]
    best_score = get_score(best_positions)

    start_time = time.time()
    while time.time() - start_time < 100:
        curr_x = best_x + np.random.normal(0, 0.05, size=num_tubes)
        curr_y = best_y + np.random.normal(0, 0.05, size=num_tubes)
        curr_positions = [curr_x, curr_y]
        curr_score = get_score(curr_positions)
        if curr_score > best_score:
            best_score = curr_score
            best_x = curr_x.copy()
            best_y = curr_y.copy()
            best_positions = [best_x, best_y]

    return np.array(best_positions)
    # EVOLVE-BLOCK-END


if __name__ == "__main__":
    result = solve(n=8)
    print("Score:", get_score(result))
