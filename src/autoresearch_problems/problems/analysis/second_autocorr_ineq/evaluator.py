"""Evaluator for the second autocorrelation inequality (C₂ constant).

The candidate program's solve() function should return a list or numpy array
of non-negative floats representing a step function on [-1/4, 1/4].

The objective is to MAXIMIZE:
  R(f) = ‖f*f‖₂² / (‖f*f‖₁ · ‖f*f‖∞)

Score: c2 / BENCHMARK  (higher is better; > 1 means a new record)
BENCHMARK = 0.8962799441554083  (found by AlphaEvolve)

This file is standalone — it does NOT import from autoresearch_problems.
"""

import numpy as np

BENCHMARK = 0.8962799441554083
MAX_CHECK_VALUE = 1e10
MIN_CHECK_VALUE = 1e-10


def _compute_c2(sequence: np.ndarray) -> float:
    """Compute C₂ lower bound R(f) for the given sequence."""
    conv = np.convolve(sequence, sequence, mode="full")
    num_points = conv.size

    max_conv_abs = float(np.max(np.abs(conv)))
    if max_conv_abs > MAX_CHECK_VALUE:
        raise ValueError(f"Convolution values exceed max: {MAX_CHECK_VALUE}")

    # L2 norm squared via piecewise-linear rule with endpoint zeros
    x_points = np.linspace(-0.5, 0.5, num_points + 2)
    x_intervals = np.diff(x_points)
    y_points = np.concatenate(([0.0], conv, [0.0]))

    l2_norm_squared = 0.0
    for i in range(num_points + 1):
        y1 = y_points[i]
        y2 = y_points[i + 1]
        h = x_intervals[i]
        l2_norm_squared += (h / 3.0) * (y1 * y1 + y1 * y2 + y2 * y2)

    if not np.isfinite(l2_norm_squared) or l2_norm_squared < MIN_CHECK_VALUE ** 2:
        raise ValueError("L2 norm squared is non-finite or too small")

    norm_1 = float(np.sum(np.abs(conv))) / float(num_points + 1)
    norm_inf = float(np.max(np.abs(conv)))

    if norm_1 <= MIN_CHECK_VALUE or norm_inf <= MIN_CHECK_VALUE:
        raise ValueError("L1 or Linf norm is too small")

    c2 = float(l2_norm_squared) / (norm_1 * norm_inf)

    if not np.isfinite(c2):
        raise ValueError("C2 is non-finite")

    return c2


def evaluate(output, **kwargs) -> dict:
    """Score a candidate step function for the second autocorrelation inequality.

    Parameters
    ----------
    output:
        A list or 1-D array-like of non-negative floats.

    Returns
    -------
    dict
        score  : c2 / BENCHMARK  (higher is better)
        valid  : True iff all constraints are satisfied
        error  : "" on success, description of first error otherwise
        metrics: dict with c2, sequence_length
    """
    try:
        if not isinstance(output, (list, np.ndarray)):
            return {
                "score": 0.0,
                "valid": False,
                "error": f"Expected list or np.ndarray, got {type(output).__name__}",
                "metrics": {},
            }

        try:
            seq = np.asarray(output, dtype=float)
        except Exception as exc:
            return {"score": 0.0, "valid": False, "error": f"Cannot convert to array: {exc}", "metrics": {}}

        if seq.ndim != 1 or len(seq) == 0:
            return {"score": 0.0, "valid": False, "error": "Sequence must be a non-empty 1-D array", "metrics": {}}

        if not np.isfinite(seq).all():
            return {"score": 0.0, "valid": False, "error": "Sequence contains NaN or Inf values", "metrics": {}}

        if np.any(seq < -MIN_CHECK_VALUE):
            return {"score": 0.0, "valid": False, "error": f"Sequence cannot contain values below {-MIN_CHECK_VALUE}", "metrics": {}}

        if np.any(seq > MAX_CHECK_VALUE):
            return {"score": 0.0, "valid": False, "error": f"Sequence cannot contain values above {MAX_CHECK_VALUE}", "metrics": {}}

        seq = np.clip(seq, MIN_CHECK_VALUE, MAX_CHECK_VALUE)

        try:
            c2 = _compute_c2(seq)
        except ValueError as exc:
            return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}

        score = c2 / BENCHMARK if BENCHMARK > 0 else 0.0

        return {
            "score": score,
            "valid": True,
            "error": "",
            "metrics": {"c2": c2, "sequence_length": len(seq)},
        }

    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": f"Unexpected error: {exc}", "metrics": {}}
