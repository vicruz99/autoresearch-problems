# Adapted from google-deepmind/alphaevolve_repository_of_problems (Apache 2.0)
"""Evaluator for the 3D Kakeya needle problem.

Given n^2 positions (x_k, y_k) for k=0..n^2-1 and index pairs (i,j) for
i,j=0..n-1, we have n^2 tubes. Each tube T_{ij} at position (x_k, y_k)
connects a unit square at z=0 to a shifted unit square at z=1.

Score = -(volume / reference_volume); higher (less negative) is better.
Uses Monte Carlo estimation of the union volume.
"""

import numpy as np


def _union_volume_mc(x_pos: np.ndarray, y_pos: np.ndarray,
                     n: int, num_samples: int = 200_000,
                     seed: int = 42) -> float:
    """Monte Carlo estimate of the union volume of n^2 tubes.

    Matches the notebook's get_score which samples in [0, 2.5] x [0, 2.5] x [0, 1].
    """
    rng = np.random.default_rng(seed)
    inv_n = 1.0 / n

    # Sample points in [0, 2.5] x [0, 2.5] x [0, 1] (matches notebook)
    xy_extent = 2.5
    pts = rng.uniform(0, 1, size=(num_samples, 3))
    pts[:, 0] *= xy_extent
    pts[:, 1] *= xy_extent

    a, b, c = pts[:, 0], pts[:, 1], pts[:, 2]

    in_union = np.zeros(num_samples, dtype=bool)
    for idx in range(n * n):
        xi = float(x_pos[idx])
        yi = float(y_pos[idx])
        ii = idx // n
        ji = idx % n

        x_min = (1 - c) * xi + c * (xi + ii * inv_n)
        x_max = (1 - c) * (xi + inv_n) + c * (xi + (ii + 1) * inv_n)
        y_min = (1 - c) * yi + c * (yi + ji * inv_n)
        y_max = (1 - c) * (yi + inv_n) + c * (yi + (ji + 1) * inv_n)

        inside = (x_min <= a) & (a <= x_max) & (y_min <= b) & (b <= y_max)
        in_union |= inside

    # Volume = fraction_in_union * bounding_box_volume
    vol = float(np.mean(in_union)) * xy_extent * xy_extent * 1.0
    return vol


def evaluate(output, cap_n: int = 8, num_samples: int = 200_000, **kwargs) -> dict:
    """Evaluate 3D Kakeya needle positions.

    Parameters
    ----------
    output : array-like, shape (2, cap_n*cap_n) or (cap_n*cap_n, 2)
        Positions: output[0] = x coords, output[1] = y coords.
    cap_n : int
        Grid size (default 8, giving 64 tubes).
    num_samples : int
        Number of Monte Carlo samples for volume estimation (default 200_000).

    Returns
    -------
    dict with keys: score, valid, error, metrics.
    """
    if not (isinstance(cap_n, int) or (isinstance(cap_n, float) and cap_n == int(cap_n))) or int(cap_n) < 2:
        return {"score": 0.0, "valid": False,
                "error": f"cap_n must be a positive integer >= 2, got cap_n={cap_n}",
                "metrics": {}}
    cap_n = int(cap_n)
    if not (isinstance(num_samples, int) or (isinstance(num_samples, float) and num_samples == int(num_samples))) or int(num_samples) < 1000:
        return {"score": 0.0, "valid": False,
                "error": f"num_samples must be an integer >= 1000, got num_samples={num_samples}",
                "metrics": {}}
    num_samples = int(num_samples)

    n = cap_n  # internal alias

    try:
        arr = np.array(output, dtype=float)

        if arr.shape == (2, n * n):
            x_pos = arr[0]
            y_pos = arr[1]
        elif arr.shape == (n * n, 2):
            x_pos = arr[:, 0]
            y_pos = arr[:, 1]
        elif arr.ndim == 1 and len(arr) == 2 * n * n:
            x_pos = arr[:n * n]
            y_pos = arr[n * n:]
        else:
            return {
                "score": 0.0,
                "valid": False,
                "error": f"Unexpected shape {arr.shape}; expected (2, {n*n})",
                "metrics": {},
            }

        vol = _union_volume_mc(x_pos, y_pos, n, num_samples=num_samples)

        # Reference: random baseline ~1/n^2 * extent^2 is hard to compute;
        # use the trivial upper bound of 1.0 as normalisation denominator.
        score = -vol

        return {
            "score": score,
            "valid": True,
            "error": "",
            "metrics": {"union_volume": vol},
        }
    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}
