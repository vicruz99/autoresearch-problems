"""Evaluator for the Finite Field Kakeya Problem.

A Kakeya set in F_p^d is a subset K ⊆ F_p^d that contains a complete line in
every direction.  Formally, for every non-zero direction v ∈ F_p^d (considered
up to scalar multiples), there exists a base point x ∈ K such that the line
  {x + t·v  mod p  :  t ∈ F_p}
is entirely contained in K.

The goal is to minimise |K|.

Following the AlphaEvolve paper ("Mathematical Discovery at Scale"), the
construction is evaluated across multiple primes p for a fixed dimension d,
and the final score is the average normalised size:
  score = average over p of  -(|K(p)| / reference_size(p, d))
Higher (less negative) is better.

solve() must accept (p, d) and return a 2-D integer array of shape (k, d) with
entries in {0,…,p-1} for the given prime p.  The evaluator calls solve for each
prime independently; the output passed to evaluate() must be a dict
{p: np.ndarray} mapping each prime to its construction.

Adapted from google-deepmind/alphaevolve_repository_of_problems (Apache 2.0).
"""

import itertools

import numpy as np

_DEFAULT_PRIMES_BY_DIM = {
    2: [3, 5, 7, 11, 13],
    3: [3, 5, 7, 11],
    4: [3, 5, 7],
    5: [3, 5],
}
_DEFAULT_PRIMES_FALLBACK = [3, 5, 7]


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


# ---------------------------------------------------------------------------
# Saraf–Sudan reference construction
# ---------------------------------------------------------------------------

def _saraf_sudan_size(p: int, d: int) -> int:
    """Size of the Saraf–Sudan / Dvir reference construction for odd prime p."""
    if p == 2:
        return p ** d

    squares = {pow(i, 2, p) for i in range(p)}
    final_set: set = set()

    for beta in range(p):
        beta_sq = (beta * beta) % p
        for s_tuple in itertools.product(squares, repeat=d - 1):
            point = tuple((s - beta_sq) % p for s in s_tuple) + (beta,)
            final_set.add(point)

    for coords in itertools.product(range(p), repeat=d - 1):
        final_set.add(coords + (0,))

    return len(final_set)


# ---------------------------------------------------------------------------
# Kakeya validity check
# ---------------------------------------------------------------------------

def _canonical_directions(p: int, d: int):
    """Yield all canonical direction vectors in F_p^d.

    A vector is canonical if its first non-zero coordinate equals 1.
    This gives exactly (p^d - 1)/(p - 1) = p^(d-1) + … + 1 directions.
    """
    for v in itertools.product(range(p), repeat=d):
        if all(x == 0 for x in v):
            continue
        first_nonzero = next(x for x in v if x != 0)
        if first_nonzero == 1:
            yield np.array(v, dtype=np.int64)


def _is_valid_kakeya(construction: np.ndarray, p: int, d: int) -> bool:
    """Return True iff *construction* is a valid Kakeya set in F_p^d."""
    pt_set = set(map(tuple, construction))

    for v in _canonical_directions(p, d):
        found = False
        for x in construction:
            line = {tuple((x + t * v) % p) for t in range(p)}
            if line <= pt_set:
                found = True
                break
        if not found:
            return False
    return True


def _evaluate_single(construction_raw, p: int, d: int) -> dict:
    """Score a single construction for one prime p in dimension d."""
    try:
        construction = np.asarray(construction_raw, dtype=np.int64)
    except Exception as exc:
        return {"score": None, "error": f"p={p}: cannot convert to array: {exc}"}

    if construction.ndim != 2 or construction.shape[1] != d:
        return {"score": None,
                "error": f"p={p}: expected shape (k, {d}), got {construction.shape}"}

    if construction.size == 0:
        return {"score": None, "error": f"p={p}: empty construction"}

    if np.any(construction < 0) or np.any(construction >= p):
        return {"score": None,
                "error": f"p={p}: entries must be in {{0, …, {p - 1}}}"}

    unique_pts = np.unique(construction, axis=0)
    k = unique_pts.shape[0]

    ref_size = _saraf_sudan_size(p, d)
    if ref_size == 0:
        return {"score": None, "error": f"p={p}: reference size is 0"}

    if not _is_valid_kakeya(unique_pts, p, d):
        return {"score": None,
                "error": f"p={p}: construction is not a valid Kakeya set",
                "set_size": k, "reference_size": ref_size}

    norm = -float(k) / float(ref_size)
    return {"score": norm, "error": "",
            "set_size": k, "reference_size": ref_size}


# ---------------------------------------------------------------------------
# Public entry-point
# ---------------------------------------------------------------------------

def evaluate(output, d: int = 3, primes=None, **kwargs) -> dict:
    """Score a candidate Kakeya set construction across multiple primes.

    Following the AlphaEvolve paper, the construction is evaluated on several
    primes p for dimension d.  The final score is the average normalised size
    -(|K(p)| / reference_size(p, d)) over all tested primes.

    Parameters
    ----------
    output:
        A dict mapping each prime p (int) to a 2-D integer array of shape
        (k, d) with entries in {0, …, p-1} representing the Kakeya set for
        that prime.
    d:
        Dimension of the vector space (positive integer ≥ 2).
    primes:
        List of prime integers to evaluate.  Defaults to a dimension-specific
        set chosen to keep evaluation tractable.

    Returns
    -------
    dict
        score   : average -(|K(p)| / reference_size(p, d)); higher is better.
        valid   : True iff every prime's construction is a valid Kakeya set.
        error   : description of the first error, or ''.
        metrics : per-prime breakdown plus aggregate statistics.
    """
    try:
        # --- parameter validation ---
        if not isinstance(d, int) or d < 1:
            return {"score": 0.0, "valid": False,
                    "error": f"d must be a positive integer, got {d!r}",
                    "metrics": {}}

        if primes is None:
            primes = _DEFAULT_PRIMES_BY_DIM.get(d, _DEFAULT_PRIMES_FALLBACK)

        primes = list(primes)
        if not primes:
            return {"score": 0.0, "valid": False,
                    "error": "primes list is empty", "metrics": {}}

        bad_primes = [p for p in primes if not _is_prime(p)]
        if bad_primes:
            return {"score": 0.0, "valid": False,
                    "error": f"Not prime: {bad_primes}", "metrics": {}}

        # --- validate output format ---
        if not isinstance(output, dict):
            return {"score": 0.0, "valid": False,
                    "error": ("output must be a dict {p: construction_array}; "
                              f"got {type(output).__name__}"),
                    "metrics": {}}

        # --- evaluate each prime ---
        per_prime: dict = {}
        scores: list = []
        errors: list = []

        for p in primes:
            if p not in output:
                errors.append(f"p={p}: missing from output dict")
                per_prime[p] = {"score": None, "error": f"missing from output"}
                continue

            result = _evaluate_single(output[p], p, d)
            per_prime[p] = result
            if result["score"] is None:
                errors.append(result["error"])
            else:
                scores.append(result["score"])

        if not scores:
            return {
                "score": 0.0,
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
        return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}
