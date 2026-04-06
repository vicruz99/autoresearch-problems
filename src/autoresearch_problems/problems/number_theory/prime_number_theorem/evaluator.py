"""Evaluator for the Prime Number Theorem partial function problem."""
import numpy as np


def evaluate(output: object, num_samples: int = 100000, **kwargs) -> dict:
    if not (isinstance(num_samples, int) or (isinstance(num_samples, float) and num_samples == int(num_samples))) or int(num_samples) < 100:
        return {"score": 0.0, "valid": False,
                "error": f"num_samples must be an integer >= 100, got num_samples={num_samples}",
                "metrics": {}}
    num_samples = int(num_samples)

    try:
        if not isinstance(output, dict):
            return {"score": 0.0, "valid": False,
                    "error": "Output must be a dict mapping int -> float", "metrics": {}}
        partial_fn = {int(k): float(v) for k, v in output.items() if int(k) > 0}
    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}

    if not partial_fn:
        return {"score": 0.0, "valid": False, "error": "Empty dict", "metrics": {}}

    # Clip extreme values for stability
    clipped = {k: float(np.clip(v, -10, 10)) for k, v in partial_fn.items()}

    # Normalize: adjust f(1) so the multiplicative constraint sum(f(k)/k)=0 holds
    total = sum(v / k for k, v in clipped.items())
    clipped[1] = clipped.get(1, 0.0) - total

    keys = np.array(list(clipped.keys()), dtype=np.float64)
    vals = np.array(list(clipped.values()), dtype=np.float64)

    max_key = np.max(keys)
    upper = 10 * max_key

    rng = np.random.default_rng(42)
    for _ in range(num_samples):
        x = rng.uniform(1, upper)
        x_sum = float(np.sum(vals * np.floor(x / keys)))
        if x_sum > 1.0001:
            return {"score": float(-np.inf), "valid": False,
                    "error": f"Constraint violated at x={x:.2f} (sum={x_sum:.4f})",
                    "metrics": {}}

    a_value = float(-np.sum(vals * np.log(keys) / keys))
    return {"score": a_value, "valid": True, "error": "",
            "metrics": {"a_value": a_value, "num_keys": len(clipped)}}
