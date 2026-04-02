"""Evaluator for the first autocorrelation inequality (C₁ constant).

The candidate program's solve() function should return a list or numpy array
of non-negative floats representing a step function on [-1/4, 1/4].

The objective is to MINIMIZE:
  c1 = 2 * n * max(conv(f, f)) / (sum(f))²

Score: BENCHMARK / c1  (higher is better; > 1 means a new record)
BENCHMARK = 1.5052939684401607  (found by AlphaEvolve)

This file is standalone — it does NOT import from autoresearch_problems.
"""

import numpy as np

BENCHMARK = 1.5052939684401607


def _compute_c1(sequence: np.ndarray) -> float:
    """Compute C₁ upper bound for the given sequence."""
    seq = [float(x) for x in sequence]
    seq = [max(0.0, x) for x in seq]
    seq = [min(10_000_000.0, x) for x in seq]

    n = len(seq)
    b_sequence = np.convolve(seq, seq)
    max_b = float(np.max(b_sequence))
    sum_a = float(np.sum(seq))

    if sum_a < 1e-9:
        return float("inf")

    return float(2 * n * max_b / (sum_a ** 2))


def evaluate(output, **kwargs) -> dict:
    """Score a candidate step function for the first autocorrelation inequality.

    Parameters
    ----------
    output:
        A list or 1-D array-like of non-negative floats.

    Returns
    -------
    dict
        score  : BENCHMARK / c1  (higher is better)
        valid  : True iff all constraints are satisfied
        error  : "" on success, description of first error otherwise
        metrics: dict with c1, sequence_length
    """
    try:
        if not isinstance(output, (list, np.ndarray)):
            return {
                "score": 0.0,
                "valid": False,
                "error": f"Expected list or np.ndarray, got {type(output).__name__}",
                "metrics": {},
            }

        if isinstance(output, np.ndarray):
            sequence = output.tolist()
        else:
            sequence = list(output)

        if not sequence:
            return {"score": 0.0, "valid": False, "error": "Sequence cannot be empty", "metrics": {}}

        for x in sequence:
            if isinstance(x, bool) or not isinstance(x, (int, float, np.number)):
                return {"score": 0.0, "valid": False, "error": "Sequence entries must be integers or floats", "metrics": {}}
            if np.isnan(x) or np.isinf(x):
                return {"score": 0.0, "valid": False, "error": "Sequence cannot contain NaN or Inf values", "metrics": {}}

        seq_array = np.array([float(x) for x in sequence])
        seq_array = np.maximum(0.0, seq_array)
        seq_array = np.minimum(10_000_000.0, seq_array)

        sum_a = float(np.sum(seq_array))
        if sum_a < 1e-5:
            return {"score": 0.0, "valid": False, "error": f"Sum of sequence too close to zero: {sum_a}", "metrics": {}}

        c1 = _compute_c1(seq_array)
        score = BENCHMARK / c1 if c1 > 0 else 0.0

        return {
            "score": score,
            "valid": True,
            "error": "",
            "metrics": {"c1": c1, "sequence_length": len(sequence)},
        }

    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": f"Unexpected error: {exc}", "metrics": {}}
