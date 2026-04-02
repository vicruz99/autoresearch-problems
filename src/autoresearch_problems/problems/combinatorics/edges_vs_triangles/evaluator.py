# Adapted from google-deepmind/alphaevolve_repository_of_problems (Apache 2.0)
"""Evaluator for the edges-vs-triangles problem.

The candidate solve() function returns a 2-D numpy array of shape (M, N)
(M ≥ 1 rows, N = 20 columns) where each row is a non-negative vector.
Rows are normalised to sum to 1 before evaluation.

For each normalised row v the edge density and triangle density are:
  edge_density      = sum_{i<j}   v_i * v_j
  triangle_density  = sum_{i<j<k} v_i * v_j * v_k

The evaluator then constructs the piecewise 'capped slope-3' density curve
and computes:
  area        = area under the capped-slope-3 boundary function
  max_gap     = maximum gap between consecutive edge densities

Score = (5/6) / (area + 10 * max_gap).  A score of 1.0 corresponds to the
theoretical minimum area = 5/6 with zero gap (Kruskal-Katona bound).
Higher scores are better.
"""

import numpy as np

# Theoretical minimum area (Kruskal-Katona)
_BENCHMARK = 5.0 / 6.0


def _sum_pairwise_triple(A: np.ndarray):
    """Compute edge and triangle 'densities' for each row of A.

    Uses the same convention as the AlphaEvolve notebook:
      pairwise = S1² - S2  (= 2 * sum_{i<j} aᵢaⱼ)
      triple   = S1³ - 3·S1·S2 + 2·S3  (= 6 * sum_{i<j<k} aᵢaⱼaₖ)
    where Sk = sum(aᵢᵏ).  For a unit-sum row, pairwise ∈ [0,1) and
    triple ∈ [0,1).
    """
    M, N = A.shape
    S1 = np.sum(A, axis=1)
    S2 = np.sum(A ** 2, axis=1)
    pairwise = S1 ** 2 - S2

    triple = np.zeros(M, dtype=A.dtype)
    if N >= 3:
        S3 = np.sum(A ** 3, axis=1)
        S1_sq = S1 ** 2
        triple = S1_sq * S1 - 3.0 * S1 * S2 + 2.0 * S3

    return pairwise, triple


def _analyze_density_curve(edge_densities: np.ndarray,
                            triangle_densities: np.ndarray):
    """Compute area under the capped slope-3 curve and max gap."""
    eps = 1e-9
    slope = 3.0

    if edge_densities.size == 0:
        return 5.0 / 6.0, 1.0

    sort_idx = np.argsort(edge_densities)
    sx = edge_densities[sort_idx]
    sy = triangle_densities[sort_idx]

    # Prepend (0,0) and append (1,1)
    full_x = np.concatenate([[0.0], sx, [1.0]])
    full_y = np.concatenate([[0.0], sy, [1.0]])

    # Remove duplicate x-values
    _, unique_idx = np.unique(full_x, return_index=True)
    full_x = full_x[unique_idx]
    full_y = full_y[unique_idx]

    total_area = 0.0
    for i in range(len(full_x) - 1):
        xi, yi = full_x[i], full_y[i]
        xn, yn = full_x[i + 1], full_y[i + 1]
        w = xn - xi
        if w < eps:
            continue

        if yi > yn + eps:
            # Case 1: decreasing → horizontal at yi
            total_area += yi * w
        else:
            y_calc = yi + slope * w
            if y_calc <= yn + eps:
                # Case 2a: slope-3 does not overshoot
                total_area += (yi + y_calc) * w / 2.0
            else:
                # Case 2b: slope-3 overshoots → ramp then flat
                delta_y = max(0.0, yn - yi)
                w1 = min(delta_y / slope, w)
                w2 = w - w1
                total_area += (yi + yn) * w1 / 2.0 + yn * w2

    # Max gap in (0, 1)
    gaps = np.diff(full_x)
    in_range = (full_x[:-1] >= 0.0) & (full_x[:-1] < 1.0)
    max_gap = float(np.max(gaps[in_range])) if np.any(in_range) else 1.0

    return float(total_area), max_gap


def evaluate(output, n: int = 20, **kwargs) -> dict:
    """Score a set of probability vectors for edges-vs-triangles.

    Parameters
    ----------
    output:
        Array-like of shape (M, N) with N = n (default 20).  Each row is a
        non-negative vector; rows are normalised to sum to 1.
    n:
        Expected vector length.

    Returns
    -------
    dict with keys: score (float), valid (bool), error (str), metrics (dict).
    """
    try:
        try:
            solutions = np.array(output, dtype=float)
        except Exception as exc:
            return {"score": 0.0, "valid": False,
                    "error": f"Cannot convert output to array: {exc}",
                    "metrics": {}}

        if solutions.ndim != 2:
            return {"score": 0.0, "valid": False,
                    "error": f"Expected 2-D array, got ndim={solutions.ndim}",
                    "metrics": {}}

        M, N = solutions.shape
        if N != n:
            return {"score": 0.0, "valid": False,
                    "error": f"Expected {n} columns, got {N}", "metrics": {}}

        if not np.isfinite(solutions).all():
            return {"score": 0.0, "valid": False,
                    "error": "Array contains NaN or Inf", "metrics": {}}

        if np.any(solutions < 0):
            return {"score": 0.0, "valid": False,
                    "error": "Negative values in probability vectors",
                    "metrics": {}}

        # Normalise rows to sum to 1; skip zero-sum rows
        row_sums = solutions.sum(axis=1)
        valid_mask = row_sums > 1e-7
        if not np.any(valid_mask):
            return {"score": 0.0, "valid": False,
                    "error": "All rows have zero sum", "metrics": {}}

        solutions = solutions[valid_mask]
        solutions = solutions / solutions.sum(axis=1, keepdims=True)

        edge_densities, triangle_densities = _sum_pairwise_triple(solutions)

        if np.any(np.isnan(edge_densities)) or np.any(np.isnan(triangle_densities)):
            return {"score": 0.0, "valid": False,
                    "error": "NaN in computed densities", "metrics": {}}

        area, max_gap = _analyze_density_curve(edge_densities, triangle_densities)

        raw_objective = area + 10.0 * max_gap
        score = float(_BENCHMARK / raw_objective) if raw_objective > 0 else 0.0

        return {
            "score": score,
            "valid": True,
            "error": "",
            "metrics": {
                "area": area,
                "max_gap": max_gap,
                "raw_objective": raw_objective,
                "num_solutions": int(solutions.shape[0]),
                "score": score,
            },
        }

    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}
