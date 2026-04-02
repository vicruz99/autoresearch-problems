# Adapted from google-deepmind/alphaevolve_repository_of_problems (Apache 2.0)
"""Evaluator for the 2D Kakeya needle problem.

Given n positions x = [x_1, ..., x_n], computes the area of the union of
triangles R_i with vertices (x_i, 0), (x_i + 1/n, 0), (x_i + i/n, 1).
Score = -(area / keich_reference_area); higher (less negative) is better.
"""

import numpy as np


def _keich_positions(n: int) -> list:
    pos = int(np.log2(n)) if n > 1 else 1
    j = np.arange(1, pos + 1)
    x = []
    for i in range(n):
        eps = np.array(list(str(bin(i))[2:]), dtype=int)
        eps = np.pad(eps, (pos - len(eps), 0), "constant")
        x.append(float(np.sum((1 - j) * eps * (2.0 ** -j) / pos)))
    return x


def _union_area(x: list) -> float:
    try:
        from shapely import geometry
    except ImportError:
        return _union_area_grid(x)

    n = len(x)
    delta = 1.0 / n
    polygons = []
    for i in range(1, n + 1):
        ai = i / n
        xi = float(x[i - 1])
        vertices = [(xi, 0), (xi + delta, 0), (xi + ai, 1)]
        polygons.append(geometry.Polygon(vertices))

    if not polygons:
        return 0.0

    union = polygons[0]
    for p in polygons[1:]:
        union = union.union(p)
    return union.area


def _union_area_grid(x: list, res: int = 500) -> float:
    n = len(x)
    delta = 1.0 / n
    triangles = []
    for i in range(1, n + 1):
        ai = i / n
        xi = float(x[i - 1])
        triangles.append([(xi, 0), (xi + delta, 0), (xi + ai, 1)])

    all_verts = [v for tri in triangles for v in tri]
    min_x = min(v[0] for v in all_verts)
    max_x = max(v[0] for v in all_verts)
    width = max_x - min_x
    if width < 1e-9:
        return 0.0

    xs = np.linspace(min_x, max_x, res)
    ys = np.linspace(0, 1, res)
    gx, gy = np.meshgrid(xs, ys)
    points = np.stack([gx.ravel(), gy.ravel()], axis=1)
    inside = np.zeros(len(points), dtype=bool)
    for tri in triangles:
        v1, v2, v3 = tri
        def cross(o, a, p):
            return (a[0]-o[0])*(p[1]-o[1]) - (a[1]-o[1])*(p[0]-o[0])
        d1 = cross(v1, v2, (points[:,0], points[:,1]))
        d2 = cross(v2, v3, (points[:,0], points[:,1]))
        d3 = cross(v3, v1, (points[:,0], points[:,1]))
        m = ~((d1 < 0) | (d2 < 0) | (d3 < 0)) | ~((d1 > 0) | (d2 > 0) | (d3 > 0))
        inside |= m
    cell_area = (width / res) * (1.0 / res)
    return float(np.sum(inside) * cell_area)


def evaluate(output, n: int = 32, **kwargs) -> dict:
    """Evaluate 2D Kakeya needle positions.

    Parameters
    ----------
    output : array-like of float, length n
        Positions x_1, ..., x_n.
    n : int
        Number of triangles (default 32).

    Returns
    -------
    dict with keys: score, valid, error, metrics.
    """
    try:
        x = list(output)
        if len(x) != n:
            return {
                "score": 0.0,
                "valid": False,
                "error": f"Expected {n} positions, got {len(x)}",
                "metrics": {},
            }
        x = [float(v) for v in x]

        area = _union_area(x)

        # Compute Keich reference area for normalisation
        keich_pos = _keich_positions(n)
        keich_area = _union_area(keich_pos)

        if keich_area < 1e-12:
            score = 0.0
        else:
            score = -(area / keich_area)

        return {
            "score": score,
            "valid": True,
            "error": "",
            "metrics": {
                "area": area,
                "keich_area": keich_area,
                "ratio": area / keich_area if keich_area > 1e-12 else None,
            },
        }
    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}
