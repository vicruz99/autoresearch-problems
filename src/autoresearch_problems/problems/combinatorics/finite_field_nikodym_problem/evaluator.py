# Adapted from google-deepmind/alphaevolve_repository_of_problems (Apache 2.0)
"""Evaluator for the Finite Field Nikodym Problem in F_q^2, q = p^2.

The candidate's solve() function must return a dict {p: np.ndarray} where
each array has shape (k, 2, 2) representing k points in F_q^2 (q = p^2).
Each point is encoded as [[x_a, x_b], [y_a, y_b]] where the coordinates are
elements of F_q = F_{p^2} = F_p[α]/(α² − w), with w the smallest quadratic
non-residue mod p.

A set N must be a valid Nikodym set: for every point x in F_q^2 there must
exist a non-zero direction v in F_q^2 such that the punctured line
    { x + t*v : t in F_q, t != 0 }
is entirely contained in N.

Following the AlphaEvolve paper ("Mathematical Discovery at Scale"), the
construction is evaluated across multiple primes p, and the final score is the
average normalised complement fraction  (|F_q^2| − |N|) / |F_q^2|  over all
tested primes.  Higher is better.

This file is standalone — it does NOT import from autoresearch_problems.
"""

import numpy as np

_DEFAULT_PRIMES = [3, 5]


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
# F_q arithmetic (q = p^2, elements represented as pairs (a, b) mod p)
# ---------------------------------------------------------------------------

def _find_non_square(p: int) -> int:
    """Return the smallest quadratic non-residue mod p."""
    for w in range(2, p):
        if pow(w, (p - 1) // 2, p) == p - 1:
            return w
    raise ValueError(f"No non-square found for p={p}")


def _build_fq_tables(p: int):
    """Build addition and multiplication lookup tables for F_q (q=p^2).

    Elements are indexed 0 … q-1: index a*p + b represents a + b·α.
    Returns (add_table, mul_table, w) where w is the non-square used.
    """
    w = _find_non_square(p)
    q = p * p
    add_table = np.empty((q, q), dtype=np.int32)
    mul_table = np.empty((q, q), dtype=np.int32)

    for ai in range(p):
        for bi in range(p):
            i = ai * p + bi
            for aj in range(p):
                for bj in range(p):
                    j = aj * p + bj
                    ra = (ai + aj) % p
                    rb = (bi + bj) % p
                    add_table[i, j] = ra * p + rb
                    # (ai + bi*α)(aj + bj*α) = (ai*aj + bi*bj*w) + (ai*bj + bi*aj)*α
                    mr = (ai * aj + bi * bj * w) % p
                    mi = (ai * bj + bi * aj) % p
                    mul_table[i, j] = mr * p + mi

    return add_table, mul_table, w


# Cache tables keyed by p so we don't rebuild per call
_TABLE_CACHE: dict = {}


def _get_tables(p: int):
    if p not in _TABLE_CACHE:
        _TABLE_CACHE[p] = _build_fq_tables(p)
    return _TABLE_CACHE[p]


# ---------------------------------------------------------------------------
# Nikodym validity check
# ---------------------------------------------------------------------------

def _is_valid_nikodym(construction_set: set, p: int, add_table, mul_table) -> bool:
    """Return True if construction_set is a valid Nikodym set in F_q^2."""
    q = p * p
    nonzero_ts = [t for t in range(q) if t != 0]

    idx_one = 1 * p + 0  # element 1 = (1, 0) in F_q

    for x1 in range(q):
        for x2 in range(q):
            found = False
            # Directions (v1=idx_one, v2=m) for m in F_q
            for m in range(q):
                all_in = True
                for t in nonzero_ts:
                    tv1 = mul_table[t, idx_one]
                    tv2 = mul_table[t, m]
                    p1 = add_table[x1, tv1]
                    p2 = add_table[x2, tv2]
                    if (p1, p2) not in construction_set:
                        all_in = False
                        break
                if all_in:
                    found = True
                    break
            if found:
                continue
            # Direction (v1=0, v2=idx_one)
            all_in = True
            for t in nonzero_ts:
                tv2 = mul_table[t, idx_one]
                p1 = x1
                p2 = add_table[x2, tv2]
                if (p1, p2) not in construction_set:
                    all_in = False
                    break
            if all_in:
                found = True
            if not found:
                return False
    return True


def _evaluate_single_nikodym(arr_raw, p: int) -> dict:
    """Score one Nikodym construction for prime p (d fixed to 2)."""
    q = p * p
    total = q * q  # |F_q^2|

    try:
        arr = np.asarray(arr_raw, dtype=np.int64)
    except Exception as exc:
        return {"score": None, "error": f"p={p}: cannot convert to array: {exc}"}

    if arr.ndim != 3 or arr.shape[1] != 2 or arr.shape[2] != 2:
        return {"score": None,
                "error": f"p={p}: expected shape (k,2,2), got {arr.shape}"}

    if arr.size > 0 and (arr.min() < 0 or arr.max() >= p):
        return {"score": None,
                "error": f"p={p}: values must be in {{0, …, {p - 1}}}"}

    unique_set: set = set()
    for row in arr:
        pt = (int(row[0, 0]) * p + int(row[0, 1]),
              int(row[1, 0]) * p + int(row[1, 1]))
        unique_set.add(pt)

    k = len(unique_set)

    add_table, mul_table, _ = _get_tables(p)

    if not _is_valid_nikodym(unique_set, p, add_table, mul_table):
        return {"score": None,
                "error": f"p={p}: not a valid Nikodym set",
                "nikodym_set_size": k, "total_space": total}

    # Normalised complement fraction so scores are comparable across primes
    norm_score = float(total - k) / float(total)
    return {"score": norm_score, "error": "",
            "nikodym_set_size": k, "complement_size": total - k,
            "total_space": total}


# ---------------------------------------------------------------------------
# Public evaluate interface
# ---------------------------------------------------------------------------

def evaluate(output, d: int = 2, primes=None, **kwargs) -> dict:
    """Score candidate Nikodym sets across multiple primes.

    Following the AlphaEvolve paper, the construction is evaluated on several
    primes p (with q = p^2) for dimension d=2.  The final score is the average
    normalised complement fraction  (|F_q^2| − |N|) / |F_q^2|.  Higher is better.

    Parameters
    ----------
    output:
        A dict mapping each prime p (int) to an integer array of shape (k, 2, 2)
        with values in {0, …, p-1}.  Each row [[xa,xb],[ya,yb]] represents a
        point in F_{p^2}^2.
    d:
        Dimension (must be 2).
    primes:
        List of primes to evaluate.  Defaults to [3, 5].

    Returns
    -------
    dict
        score   : average normalised complement fraction; higher is better.
        valid   : True iff every prime's construction is a valid Nikodym set.
        error   : "" on success, description of first problem otherwise.
        metrics : per-prime breakdown plus aggregate statistics.
    """
    try:
        if d != 2:
            return {"score": 0, "valid": False,
                    "error": "Only d=2 is supported", "metrics": {}}

        if primes is None:
            primes = _DEFAULT_PRIMES

        primes = list(primes)
        if not primes:
            return {"score": 0, "valid": False,
                    "error": "primes list is empty", "metrics": {}}

        bad_primes = [p for p in primes if not _is_prime(p)]
        if bad_primes:
            return {"score": 0, "valid": False,
                    "error": f"Not prime: {bad_primes}", "metrics": {}}

        if not isinstance(output, dict):
            return {"score": 0, "valid": False,
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

            result = _evaluate_single_nikodym(output[p], p)
            per_prime[p] = result
            if result["score"] is None:
                errors.append(result["error"])
            else:
                scores.append(result["score"])

        if not scores:
            return {
                "score": 0,
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
        return {"score": 0, "valid": False,
                "error": f"Unexpected error: {exc}", "metrics": {}}
