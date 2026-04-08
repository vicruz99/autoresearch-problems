"""Evaluator for the second autocorrelation inequality (C₂ constant).

The candidate program's solve() function should return a list or numpy array
of non-negative floats representing a step function on [-1/4, 1/4].

The objective is to MAXIMIZE:
  C₂ = ‖f*f‖₂² / (‖f*f‖₁ · ‖f*f‖∞)

Score: raw c2 value (higher is better). AlphaEvolve achieved C₂ ≥ 0.8963.

This file is standalone — it does NOT import from autoresearch_problems.
"""

import numpy as np

_CLIP_MAX = 10_000_000


def _compute_c2(sequence: np.ndarray) -> float:
    """Compute C₂ lower bound for the given non-negative sequence."""
    b = np.convolve(sequence, sequence)
    sum_b = float(np.sum(b))
    max_b = float(np.max(b))
    c2 = float(np.sum(b ** 2)) / (sum_b * max_b)
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
        score  : raw c2 value (higher is better)
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

        if np.all(seq == 0):
            return {"score": 0.0, "valid": False, "error": "Sequence must not be all zeros", "metrics": {}}

        seq = np.clip(seq, 0, _CLIP_MAX)

        try:
            c2 = _compute_c2(seq)
        except (ValueError, ZeroDivisionError) as exc:
            return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}

        return {
            "score": float(c2),
            "valid": True,
            "error": "",
            "metrics": {"c2": float(c2), "sequence_length": len(seq)},
        }

    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": f"Unexpected error: {exc}", "metrics": {}}
