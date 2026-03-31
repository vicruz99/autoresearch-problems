"""Evaluator for the Cap Set problem.

A cap set in F_q^n is a subset with no three-term arithmetic progression,
i.e. no x, y, z (not necessarily distinct) such that x + y + z ≡ 0 (mod q).

The evaluator receives the candidate set as a 2-D integer array of shape
(k, n) where each row is a vector in F_q^n, and returns the set size k as
the score if no arithmetic progression is present, else 0.

This file is standalone and library-agnostic — it does NOT import from
autoresearch_problems.  The only dependency is numpy.
"""

from __future__ import annotations

import numpy as np


def evaluate(output: object, n: int = 8, q: int = 3, **kwargs) -> dict:
    """Score a candidate cap set.

    Parameters
    ----------
    output:
        A 2-D array-like of shape ``(k, n)`` with integer entries in
        ``{0, 1, …, q-1}``.
    n:
        Dimension of the vector space.
    q:
        Field size (default 3 for GF(3)).

    Returns
    -------
    dict
        ``score`` = size of the set if valid, else 0.
        ``valid`` = True iff the set contains no arithmetic progression.
        ``error`` = description of the first error found, or empty string.
        ``metrics`` = dict with extra info (e.g. ``set_size``).
    """
    try:
        S = np.asarray(output, dtype=int)
    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": f"Cannot convert output to array: {exc}", "metrics": {}}

    if S.ndim != 2 or S.shape[1] != n:
        return {
            "score": 0.0,
            "valid": False,
            "error": f"Expected shape (k, {n}), got {S.shape}",
            "metrics": {},
        }

    if S.size == 0:
        return {"score": 0.0, "valid": True, "error": "", "metrics": {"set_size": 0}}

    if np.any((S < 0) | (S >= q)):
        return {
            "score": 0.0,
            "valid": False,
            "error": f"All entries must be in {{0, …, {q - 1}}}",
            "metrics": {},
        }

    k = S.shape[0]

    # Check for duplicate rows
    if len({tuple(row) for row in S}) < k:
        return {"score": 0.0, "valid": False, "error": "Duplicate vectors in the set", "metrics": {}}

    # Check every triple (i, j, k) with i < j for arithmetic progressions.
    # x + y + z ≡ 0 (mod q) iff z ≡ -(x+y) (mod q).
    # We build a lookup set for fast membership testing.
    row_set = {tuple(row) for row in S}

    for i in range(k):
        for j in range(i + 1, k):
            # The third element needed to form a progression with S[i] and S[j]:
            # S[i] + S[j] + z ≡ 0 => z ≡ -(S[i] + S[j]) (mod q)
            z = tuple(int(-(S[i, d] + S[j, d])) % q for d in range(n))
            if z in row_set and z != tuple(S[i]) and z != tuple(S[j]):
                return {
                    "score": 0.0,
                    "valid": False,
                    "error": f"Arithmetic progression found: {S[i]}, {S[j]}, {np.array(z)}",
                    "metrics": {},
                }

    return {"score": float(k), "valid": True, "error": "", "metrics": {"set_size": k}}
