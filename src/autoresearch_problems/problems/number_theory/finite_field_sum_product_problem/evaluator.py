# Adapted from google-deepmind/alphaevolve_repository_of_problems (Apache 2.0)
"""Evaluator for the Finite Field Sum-Product Problem.

The candidate's solve() function must return a dict {p: np.ndarray} where each
array has shape (k,) with k = floor(sqrt(p)) containing distinct elements from
{0, 1, …, p−1} in the finite field F_p.

The objective is to MINIMISE  max(|X+X|, |X·X|)  where
    X + X = {(a + b) mod p : a, b ∈ X}
    X · X = {(a * b) mod p : a, b ∈ X}

Following the AlphaEvolve paper ("Mathematical Discovery at Scale"), the
construction is evaluated across multiple primes.  For each prime p, the
normalised score is:
    log(max(|X+X|, |X·X|)) / log(|X|)
and the final score is the average of these normalised scores.  Lower is better.

This file is standalone — it does NOT import from autoresearch_problems.
"""

import math
import numpy as np

_DEFAULT_PRIMES = [101, 257, 1009]  # primes ≡ 1 mod 4 for AlphaEvolve compatibility


# ---------------------------------------------------------------------------
# Primality check
# ---------------------------------------------------------------------------

def _is_prime(n: int) -> bool:
    """Return True iff n is a prime number."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def _sum_prod_sizes(x: np.ndarray, p: int):
    """Return (|X+X|, |X·X|) for set X ⊆ F_p."""
    n = len(x)
    i_idx, j_idx = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
    sums = (x[i_idx] + x[j_idx]) % p
    prods = (x[i_idx] * x[j_idx]) % p
    return len(np.unique(sums)), len(np.unique(prods))


def _evaluate_single_sum_product(arr_raw, p: int) -> dict:
    """Score one sum-product construction for prime p."""
    target_size = int(math.sqrt(p))

    try:
        arr = np.asarray(arr_raw, dtype=np.int64).ravel()
    except Exception as exc:
        return {"score": None, "error": f"p={p}: cannot convert to array: {exc}"}

    if arr.shape[0] != target_size:
        return {"score": None,
                "error": f"p={p}: expected size {target_size}, got {arr.shape[0]}"}

    if arr.min() < 0 or arr.max() >= p:
        return {"score": None,
                "error": f"p={p}: elements must be in {{0, …, {p - 1}}}"}

    if len(np.unique(arr)) != target_size:
        return {"score": None,
                "error": f"p={p}: construction contains duplicate elements"}

    sum_size, prod_size = _sum_prod_sizes(arr, p)
    raw_score = max(sum_size, prod_size)

    # Normalised score as per the paper: log(max(|A+A|,|A·A|)) / log(|A|)
    norm_score = math.log(raw_score) / math.log(target_size)

    return {"score": norm_score, "error": "",
            "sum_set_size": sum_size, "prod_set_size": prod_size,
            "set_size": target_size, "raw_score": raw_score}


# ---------------------------------------------------------------------------
# Public entry-point
# ---------------------------------------------------------------------------

def evaluate(output, primes=None, **kwargs) -> dict:
    """Score candidate sum-product constructions across multiple primes.

    Following the AlphaEvolve paper, the construction is evaluated on several
    primes p.  For each p, the normalised score is
        log(max(|X+X|, |X·X|)) / log(|X|)
    and the final score is the average of these values.  Lower is better.

    Parameters
    ----------
    output:
        A dict mapping each prime p (int) to a 1-D integer array of length
        floor(sqrt(p)) with distinct values in {0, …, p-1}.
    primes:
        List of primes to evaluate.  Defaults to [101, 257, 1009].

    Returns
    -------
    dict
        score   : average log-normalised score; lower is better.
        valid   : True iff every prime's construction is valid.
        error   : "" on success, description of first problem otherwise.
        metrics : per-prime breakdown plus aggregate statistics.
    """
    try:
        if primes is None:
            primes = _DEFAULT_PRIMES

        primes = list(primes)
        if not primes:
            return {"score": float("inf"), "valid": False,
                    "error": "primes list is empty", "metrics": {}}

        bad_primes = [p for p in primes if not _is_prime(p)]
        if bad_primes:
            return {"score": float("inf"), "valid": False,
                    "error": f"Not prime: {bad_primes}", "metrics": {}}

        if not isinstance(output, dict):
            return {"score": float("inf"), "valid": False,
                    "error": ("output must be a dict {p: construction_array}; "
                              f"got {type(output).__name__}"),
                    "metrics": {}}

        per_prime: dict = {}
        scores: list = []
        errors: list = []

        for p in primes:
            if p not in output:
                errors.append(f"p={p}: missing from output dict")
                per_prime[p] = {"score": None, "error": "missing from output"}
                continue

            result = _evaluate_single_sum_product(output[p], p)
            per_prime[p] = result
            if result["score"] is None:
                errors.append(result["error"])
            else:
                scores.append(result["score"])

        if not scores:
            return {
                "score": float("inf"),
                "valid": False,
                "error": "; ".join(errors) if errors else "no valid constructions",
                "metrics": {"per_prime": per_prime},
            }

        avg_score = sum(scores) / len(scores)
        all_valid = len(errors) == 0

        return {
            "score": avg_score,
            "valid": all_valid,
            "error": "; ".join(errors) if errors else "",
            "metrics": {
                "per_prime": per_prime,
                "avg_normalized_score": avg_score,
                "num_valid_primes": len(scores),
                "num_primes": len(primes),
            },
        }

    except Exception as exc:
        return {
            "score": float("inf"),
            "valid": False,
            "error": f"Unexpected error: {exc}",
            "metrics": {},
        }
