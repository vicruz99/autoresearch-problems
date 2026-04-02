"""Evaluator for the Circle Packing (maximize sum of radii) problem."""
import numpy as np


def evaluate(output: object, n: int = 26, **kwargs) -> dict:
    try:
        arr = np.asarray(output, dtype=float)
    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}
    if arr.ndim != 2 or arr.shape != (n, 3):
        return {"score": 0.0, "valid": False,
                "error": f"Expected ({n}, 3), got {arr.shape}", "metrics": {}}

    cx, cy, r = arr[:, 0], arr[:, 1], arr[:, 2]

    if np.any(r <= 0):
        return {"score": 0.0, "valid": False, "error": "All radii must be positive", "metrics": {}}

    # Check circles are inside [0,1]^2
    if (np.any(cx - r < -1e-9) or np.any(cx + r > 1 + 1e-9)
            or np.any(cy - r < -1e-9) or np.any(cy + r > 1 + 1e-9)):
        return {"score": 0.0, "valid": False,
                "error": "All circles must fit inside the unit square [0,1]^2", "metrics": {}}

    # Check no two circles overlap
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.sqrt((cx[i] - cx[j]) ** 2 + (cy[i] - cy[j]) ** 2)
            if dist < r[i] + r[j] - 1e-9:
                return {"score": 0.0, "valid": False,
                        "error": f"Circles {i} and {j} overlap (dist={dist:.4f} < {r[i]+r[j]:.4f})",
                        "metrics": {}}

    total_r = float(np.sum(r))
    return {"score": total_r, "valid": True, "error": "",
            "metrics": {"sum_of_radii": total_r, "min_radius": float(np.min(r)),
                        "max_radius": float(np.max(r))}}
