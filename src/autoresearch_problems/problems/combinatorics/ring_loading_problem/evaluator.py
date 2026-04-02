"""Evaluator for the Ring Loading Problem."""
import itertools


def _compute_alpha(u, v):
    m = len(u)
    if m == 0:
        return 0.0
    best_alpha = float("inf")
    z_choices = [(vi, -ui) for ui, vi in zip(u, v)]
    for z in itertools.product(*z_choices):
        z = list(z)
        max_imbalance = 0.0
        for k in range(1, m):
            left = sum(z[:k])
            right = sum(z[k:])
            max_imbalance = max(max_imbalance, abs(left - right))
        best_alpha = min(best_alpha, max_imbalance)
    return best_alpha


def evaluate(output: object, m: int = 15, **kwargs) -> dict:
    try:
        params = list(output)
        if len(params) != m:
            return {"score": 0.0, "valid": False,
                    "error": f"Expected {m} pairs, got {len(params)}", "metrics": {}}
    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}

    u, v = [], []
    for item in params:
        try:
            ui, vi = abs(float(item[0])), abs(float(item[1]))
        except Exception:
            return {"score": 0.0, "valid": False,
                    "error": "Each item must be an (u, v) pair of numbers", "metrics": {}}
        s = ui + vi
        if s > 1.0 + 1e-9:
            # Normalize so u+v <= 1
            ui /= s
            vi /= s
        u.append(ui)
        v.append(vi)

    try:
        alpha = _compute_alpha(u, v)
        return {"score": alpha, "valid": True, "error": "",
                "metrics": {"alpha": alpha}}
    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}
