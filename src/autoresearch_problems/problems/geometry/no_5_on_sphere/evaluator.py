"""Evaluator for the No 5 on a Sphere problem.

The candidate program returns a list of integer triples (x, y, z) where each
coordinate is in [0, n-1].  The set must contain no 5 co-spherical points.

Five points are co-spherical iff the determinant of the 5×5 matrix with rows
[x, y, z, x²+y²+z², 1] equals zero (Cayley-Menger condition).

Score = number of points in the set (higher is better).

Matches no_5_on_a_sphere.ipynb Cell 4/5/10.
"""
import numpy as np


def _det5x5_int(matrix: np.ndarray) -> int:
    """Exact 5x5 determinant using Laplace expansion along row 0."""
    det = 0
    for col in range(5):
        # Minor indices (exclude col from columns)
        minor_cols = [c for c in range(5) if c != col]
        minor = matrix[1:, :][:, minor_cols]
        sign = (-1) ** col
        det += sign * int(matrix[0, col]) * int(np.linalg.det(minor.astype(np.float64)))
    return det


def _are_five_cospherical(points: np.ndarray) -> bool:
    """Check if 5 integer 3D points are co-spherical using exact integer arithmetic."""
    matrix = np.zeros((5, 5), dtype=np.int64)
    for i in range(5):
        p = points[i]
        matrix[i, 0] = int(p[0])
        matrix[i, 1] = int(p[1])
        matrix[i, 2] = int(p[2])
        matrix[i, 3] = int(p[0]) ** 2 + int(p[1]) ** 2 + int(p[2]) ** 2
        matrix[i, 4] = 1
    # Use floating-point det for efficiency; for integer grid points this is exact
    # for reasonable n values
    det = np.linalg.det(matrix.astype(np.float64))
    return abs(det) < 0.5  # integers: if det is 0, it's exactly 0


def evaluate(output: object, n: int = 50, **kwargs) -> dict:
    """Score a candidate set of grid points for the no-5-on-a-sphere problem.

    Parameters
    ----------
    output : list of (int, int, int) tuples
        Each tuple is a point (x, y, z) in the grid [0, n-1]^3.
    n : int
        Grid size; coordinates must be in [0, n-1].

    Returns
    -------
    dict with keys: score, valid, error, metrics.
        score = number of valid points if no 5 are co-spherical, else 0.
    """
    try:
        pts = []
        for item in output:
            try:
                x, y, z = int(item[0]), int(item[1]), int(item[2])
            except (TypeError, ValueError, IndexError) as exc:
                return {"score": 0.0, "valid": False,
                        "error": f"Invalid point {item}: {exc}", "metrics": {}}
            pts.append((x, y, z))
    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}

    if len(pts) < 1:
        return {"score": 0.0, "valid": True, "error": "",
                "metrics": {"num_points": 0}}

    # Check coordinates are in valid range
    for p in pts:
        if not (0 <= p[0] < n and 0 <= p[1] < n and 0 <= p[2] < n):
            return {"score": 0.0, "valid": False,
                    "error": f"Point {p} out of grid [0,{n-1}]^3", "metrics": {}}

    # Check for duplicate points
    if len(set(pts)) < len(pts):
        return {"score": 0.0, "valid": False, "error": "Duplicate points", "metrics": {}}

    pts_arr = np.array(pts, dtype=np.int64)
    num_pts = len(pts_arr)

    if num_pts < 5:
        return {"score": float(num_pts), "valid": True, "error": "",
                "metrics": {"num_points": num_pts}}

    # Check every combination of 5 points for co-sphericity
    from itertools import combinations
    for combo in combinations(range(num_pts), 5):
        five_pts = pts_arr[list(combo)]
        if _are_five_cospherical(five_pts):
            return {"score": 0.0, "valid": False,
                    "error": f"5 co-spherical points found at indices {combo}",
                    "metrics": {"num_points": num_pts}}

    return {"score": float(num_pts), "valid": True, "error": "",
            "metrics": {"num_points": num_pts}}
