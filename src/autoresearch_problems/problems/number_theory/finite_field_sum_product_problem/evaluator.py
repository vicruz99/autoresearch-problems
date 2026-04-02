# Adapted from google-deepmind/alphaevolve_repository_of_problems (Apache 2.0)
"""Evaluator for the Finite Field Sum-Product Problem.

The candidate's solve() function must return a 1-D integer NumPy array of
shape (k,) where k = floor(sqrt(p)), containing exactly k distinct elements
from {0, 1, …, p−1} in the finite field F_p.

The objective is to MINIMISE  max(|X+X|, |X·X|)  where
    X + X = {(a + b) mod p : a, b ∈ X}
    X · X = {(a * b) mod p : a, b ∈ X}

Score = max(|X+X|, |X·X|).  Lower is better.

This file is standalone — it does NOT import from autoresearch_problems.
"""

import math
import numpy as np

_DEFAULT_P = 1009  # prime ≡ 1 mod 4


def _sum_prod_sizes(x: np.ndarray, p: int):
    """Return (|X+X|, |X·X|) for set X ⊆ F_p.

    Parameters
    ----------
    x : 1-D int64 array of distinct elements in {0,…,p-1}
    p : prime
    """
    n = len(x)
    # Compute all pairwise sums and products
    i_idx, j_idx = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
    sums = (x[i_idx] + x[j_idx]) % p
    prods = (x[i_idx] * x[j_idx]) % p
    sum_size = len(np.unique(sums))
    prod_size = len(np.unique(prods))
    return sum_size, prod_size


def evaluate(output, p: int = _DEFAULT_P, **kwargs) -> dict:
    """Score a candidate set X ⊆ F_p.

    Parameters
    ----------
    output:
        A 1-D integer array-like of length k = floor(sqrt(p)) with distinct
        values in {0, …, p−1}.
    p:
        Prime order of the field.

    Returns
    -------
    dict
        score   : max(|X+X|, |X·X|)  – **lower is better**
        valid   : True iff the array has correct size, no duplicates, in F_p
        error   : "" on success, description of first problem otherwise
        metrics : dict with sum_set_size, prod_set_size, set_size
    """
    try:
        target_size = int(math.sqrt(p))

        try:
            arr = np.asarray(output, dtype=np.int64).ravel()
        except Exception as exc:
            return {
                "score": float("inf"),
                "valid": False,
                "error": f"Cannot convert to int64 array: {exc}",
                "metrics": {},
            }

        if arr.shape[0] != target_size:
            return {
                "score": float("inf"),
                "valid": False,
                "error": f"Expected size {target_size}, got {arr.shape[0]}",
                "metrics": {},
            }

        if arr.min() < 0 or arr.max() >= p:
            return {
                "score": float("inf"),
                "valid": False,
                "error": f"Elements must be in {{0, …, {p-1}}}",
                "metrics": {},
            }

        if len(np.unique(arr)) != target_size:
            return {
                "score": float("inf"),
                "valid": False,
                "error": "Construction contains duplicate elements",
                "metrics": {},
            }

        sum_size, prod_size = _sum_prod_sizes(arr, p)
        score = float(max(sum_size, prod_size))

        return {
            "score": score,
            "valid": True,
            "error": "",
            "metrics": {
                "sum_set_size": sum_size,
                "prod_set_size": prod_size,
                "set_size": target_size,
            },
        }

    except Exception as exc:
        return {
            "score": float("inf"),
            "valid": False,
            "error": f"Unexpected error: {exc}",
            "metrics": {},
        }
