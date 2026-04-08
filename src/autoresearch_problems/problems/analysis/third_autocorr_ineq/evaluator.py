"""Evaluator for the third autocorrelation inequality (C₃ constant).

The candidate program's solve() function should return a list or numpy array
of floats (can be positive or negative) representing a step function on
[-1/4, 1/4].

The objective is to MINIMIZE:
  C₃ = 2·n·max(|f*f|) / (Σ|f|)²

Score: raw c3 value (lower is better). AlphaEvolve achieved C₃ ≤ 1.4556.

This file is standalone — it does NOT import from autoresearch_problems.
"""

import numpy as np


def _compute_c3(sequence: np.ndarray) -> float:
    """Compute C₃ upper bound for the given sequence."""
    n = len(sequence)
    b = np.convolve(sequence, sequence)
    max_abs_b = float(np.max(np.abs(b)))
    sum_abs = float(np.sum(np.abs(sequence)))
    c3 = 2 * n * max_abs_b / (sum_abs ** 2)
    if not np.isfinite(c3):
        raise ValueError("C3 is non-finite")
    return c3


def evaluate(output, **kwargs) -> dict:
    """Score a candidate step function for the third autocorrelation inequality.

    Parameters
    ----------
    output:
        A list or 1-D array-like of floats (can be positive or negative).

    Returns
    -------
    dict
        score  : raw c3 value (lower is better)
        valid  : True iff all constraints are satisfied
        error  : "" on success, description of first error otherwise
        metrics: dict with c3, sequence_length
    """
    try:
        if not isinstance(output, (list, np.ndarray)):
            return {
                "score": float("inf"),
                "valid": False,
                "error": f"Expected list or np.ndarray, got {type(output).__name__}",
                "metrics": {},
            }

        try:
            seq = np.asarray(output, dtype=float)
        except Exception as exc:
            return {"score": float("inf"), "valid": False, "error": f"Cannot convert to array: {exc}", "metrics": {}}

        if seq.ndim != 1 or len(seq) == 0:
            return {"score": float("inf"), "valid": False, "error": "Sequence must be a non-empty 1-D array", "metrics": {}}

        if not np.isfinite(seq).all():
            return {"score": float("inf"), "valid": False, "error": "Sequence contains NaN or Inf values", "metrics": {}}

        sum_abs = float(np.sum(np.abs(seq)))
        if sum_abs == 0:
            return {"score": float("inf"), "valid": False, "error": "Sum of |values| is zero; invalid for C3 objective", "metrics": {}}

        try:
            c3 = _compute_c3(seq)
        except ValueError as exc:
            return {"score": float("inf"), "valid": False, "error": str(exc), "metrics": {}}

        return {
            "score": float(c3),
            "valid": True,
            "error": "",
            "metrics": {"c3": float(c3), "sequence_length": len(seq)},
        }

    except Exception as exc:
        return {"score": float("inf"), "valid": False, "error": f"Unexpected error: {exc}", "metrics": {}}
