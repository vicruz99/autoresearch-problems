"""Evaluator for the First Autocorrelation Inequality problem.

For any function f: ℝ → ℝ, define the autoconvolution f*f(t) := ∫ f(t-x)f(x) dx.

Let C₁ denote the largest constant for which:
    max_{-1/2 ≤ t ≤ 1/2} f*f(t) ≥ C₁ (∫_{-1/4}^{1/4} f(x) dx)²

holds for all non-negative f.  A step function discretized over num_intervals
equally-spaced intervals on [-1/4, 1/4] is used to construct an upper bound
on C₁.  Lower C₁ is better (minimize=True).

This file is standalone and library-agnostic — it does NOT import from
autoresearch_problems.  The only dependency is numpy.
"""

import numpy as np


def evaluate(output: object, num_intervals: int = 600, **kwargs) -> dict:
    """Score a candidate step function for the first autocorrelation inequality.

    Parameters
    ----------
    output:
        A list of ``num_intervals`` non-negative floats representing the step
        function values on equally-spaced intervals over [-1/4, 1/4].
    num_intervals:
        Expected number of intervals (default 600).

    Returns
    -------
    dict
        ``score``   = C₁ ratio (lower is better); ``float("inf")`` if invalid.
        ``valid``   = True iff the sequence passes all validation checks.
        ``error``   = description of the first error found, or empty string.
        ``metrics`` = dict with ``c1``, ``sequence_length``, ``integral_f``,
                      and ``max_autoconv`` when valid; empty dict otherwise.
    """
    # --- validation ---
    sequence = output
    if not isinstance(sequence, list):
        return {
            "score": float("inf"),
            "valid": False,
            "error": f"Sequence type expected to be list, received {type(sequence)}",
            "metrics": {},
        }
    if not sequence:
        return {
            "score": float("inf"),
            "valid": False,
            "error": "Sequence cannot be None or empty.",
            "metrics": {},
        }
    for x in sequence:
        if isinstance(x, bool) or not isinstance(x, (int, float, np.number)):
            return {
                "score": float("inf"),
                "valid": False,
                "error": "Sequence entries must be integers or floats.",
                "metrics": {},
            }
        if np.isnan(x) or np.isinf(x):
            return {
                "score": float("inf"),
                "valid": False,
                "error": "Sequence cannot contain nans or infs.",
                "metrics": {},
            }

    f_values = np.abs(np.array(sequence, dtype=np.float64))
    if np.sum(f_values) < 1e-6:
        return {
            "score": float("inf"),
            "valid": False,
            "error": "Sequence cannot be all zeros.",
            "metrics": {},
        }

    # --- compute C₁ ---
    n = len(f_values)
    domain_width = 0.5  # f is supported on [-1/4, 1/4], width = 1/2
    dx = domain_width / n
    integral_f = float(np.sum(f_values) * dx)
    if integral_f < 1e-12:
        return {
            "score": float("inf"),
            "valid": False,
            "error": "Integral of f is effectively zero.",
            "metrics": {},
        }

    autoconv = np.convolve(f_values, f_values) * dx
    max_autoconv = float(np.max(autoconv))
    c1 = max_autoconv / (integral_f ** 2)

    return {
        "score": float(c1),
        "valid": True,
        "error": "",
        "metrics": {
            "c1": float(c1),
            "sequence_length": n,
            "integral_f": integral_f,
            "max_autoconv": max_autoconv,
        },
    }
