"""Evaluator for the third autocorrelation inequality (C₃ constant).

The candidate program's solve() function should return a list or numpy array
of floats (can be positive or negative) representing a step function on
[-1/4, 1/4].

The objective is to MINIMIZE:
  C₃ = 2·n·max(|f*f|) / (∑f)²

Score: BENCHMARK / c3  (higher is better; > 1 means a new record)
BENCHMARK = 1.4556427953745406  (found by AlphaEvolve)

This file is standalone — it does NOT import from autoresearch_problems.
"""

import numpy as np

BENCHMARK = 1.4556427953745406
MAX_CHECK_VALUE = 1e10
MIN_CHECK_VALUE = 1e-10


def _compute_c3(sequence: np.ndarray) -> float:
    """Compute C₃ upper bound for the given sequence."""
    conv = np.convolve(sequence, sequence, mode="full")

    max_conv_abs = float(np.max(np.abs(conv)))
    if max_conv_abs > MAX_CHECK_VALUE:
        raise ValueError(f"Convolution values exceed max: {MAX_CHECK_VALUE}")

    sum_heights = float(np.sum(sequence))
    sum_squared = sum_heights ** 2

    c3 = abs(2 * len(sequence) * max_conv_abs / sum_squared)

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
        score  : BENCHMARK / c3  (higher is better)
        valid  : True iff all constraints are satisfied
        error  : "" on success, description of first error otherwise
        metrics: dict with c3, sequence_length
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

        if np.any(np.abs(seq) > MAX_CHECK_VALUE):
            return {"score": 0.0, "valid": False, "error": f"Sequence contains values above {MAX_CHECK_VALUE}", "metrics": {}}

        total = float(np.sum(seq))
        if abs(total) < MIN_CHECK_VALUE:
            return {"score": 0.0, "valid": False, "error": "Sum of heights is zero; invalid for C3 objective", "metrics": {}}

        if total ** 2 < MIN_CHECK_VALUE:
            return {"score": 0.0, "valid": False, "error": f"Sum squared is too small (< {MIN_CHECK_VALUE}); invalid for C3 objective", "metrics": {}}

        try:
            c3 = _compute_c3(seq)
        except ValueError as exc:
            return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}

        score = BENCHMARK / c3 if c3 > 0 else 0.0

        return {
            "score": score,
            "valid": True,
            "error": "",
            "metrics": {"c3": c3, "sequence_length": len(seq)},
        }

    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": f"Unexpected error: {exc}", "metrics": {}}
