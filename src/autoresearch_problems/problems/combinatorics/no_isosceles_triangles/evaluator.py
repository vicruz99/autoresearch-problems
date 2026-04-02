"""Evaluator for the No Isosceles Triangles problem."""
import itertools


def evaluate(output: object, n: int = 64, **kwargs) -> dict:
    try:
        points = [(int(p[0]), int(p[1])) for p in output]
    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}

    if len(points) == 0:
        return {"score": 0.0, "valid": False, "error": "No points provided", "metrics": {}}

    # Check all points are in the grid
    for x, y in points:
        if not (0 <= x < n and 0 <= y < n):
            return {"score": 0.0, "valid": False,
                    "error": f"Point ({x},{y}) is outside the {n}x{n} grid", "metrics": {}}

    # Check no duplicates
    if len(set(points)) != len(points):
        return {"score": 0.0, "valid": False, "error": "Duplicate points found", "metrics": {}}

    def dsq(p, q):
        return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2

    # Check no isosceles: for every ordered triple (a, b, c), dist(a,b) != dist(b,c)
    for a, b, c in itertools.permutations(points, 3):
        if dsq(a, b) == dsq(b, c):
            return {"score": 0.0, "valid": False,
                    "error": f"Isosceles triple found: a={a}, b={b}, c={c}", "metrics": {}}

    score = float(len(points)) / n
    return {"score": score, "valid": True, "error": "",
            "metrics": {"num_points": len(points), "normalized_score": score}}
