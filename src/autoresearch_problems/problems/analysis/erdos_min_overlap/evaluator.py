"""Evaluator for the Erdős minimum overlap problem.

The candidate program's solve() function should return a step function
h: [0, 2] → [0, 1] represented as a numpy array (or list) of n values,
where each value h[i] corresponds to the interval [2i/n, 2(i+1)/n).

Constraints:
  - h values must be in [0, 1]
  - ∫ h(x) dx = 1  (i.e., sum(h) * dx = 1 where dx = 2/n)

Score: raw c5 value (lower is better). AlphaEvolve achieved C₅ ≤ 0.3809.

This file is standalone — it does NOT import from autoresearch_problems.
"""

import numpy as np


def _compute_c5(sequence: np.ndarray) -> float:
    """Compute the C5 upper bound for the given step-function heights."""
    convolution_values = np.correlate(sequence, 1 - sequence, mode="full")
    return float(np.max(convolution_values) / len(sequence) * 2)


def evaluate(output, **kwargs) -> dict:
    """Score a candidate step function for the Erdős minimum overlap problem.

    Parameters
    ----------
    output:
        A 1-D array-like of floats representing h values in [0, 1], with
        length n > 0 and sum(output) * (2/n) ≈ 1.

    Returns
    -------
    dict
        score  : raw c5 value (lower is better)
        valid  : True iff all constraints are satisfied
        error  : "" on success, description of first error otherwise
        metrics: dict with c5, sequence_length
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

        if np.any(seq < 0) or np.any(seq > 1):
            return {
                "score": float("inf"),
                "valid": False,
                "error": f"h(x) values must be in [0, 1]; range was [{seq.min():.4g}, {seq.max():.4g}]",
                "metrics": {},
            }

        dx = 2.0 / len(seq)
        integral = float(np.sum(seq) * dx)
        if not np.isclose(integral, 1.0, atol=1e-4):
            return {
                "score": float("inf"),
                "valid": False,
                "error": f"Integral of h must be 1.0; got {integral:.6f}",
                "metrics": {},
            }

        c5 = _compute_c5(seq)

        return {
            "score": float(c5),
            "valid": True,
            "error": "",
            "metrics": {"c5": float(c5), "sequence_length": len(seq)},
        }

    except Exception as exc:
        return {"score": float("inf"), "valid": False, "error": f"Unexpected error: {exc}", "metrics": {}}
