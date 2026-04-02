"""Evaluator for the Finite Field Kakeya Problem.

A Kakeya set in F_p^d is a subset K ⊆ F_p^d that contains a complete line in
every direction.  Formally, for every non-zero direction v ∈ F_p^d (considered
up to scalar multiples), there exists a base point x ∈ K such that the line
  {x + t·v  mod p  :  t ∈ F_p}
is entirely contained in K.

The goal is to minimise |K|.  Score = -(|K| / |reference|) where the reference
is the Saraf–Sudan construction size; higher (less negative) is better.

solve() must return a 2-D integer array of shape (k, d) with entries in {0,…,p-1}.

Adapted from google-deepmind/alphaevolve_repository_of_problems (Apache 2.0).
"""

import itertools

import numpy as np


# ---------------------------------------------------------------------------
# Saraf–Sudan reference construction
# ---------------------------------------------------------------------------

def _saraf_sudan_size(p: int, d: int) -> int:
    """Size of the Saraf–Sudan / Dvir reference construction for odd prime p."""
    if p % 2 == 0 or p < 2:
        # Fallback: full space (trivially a Kakeya set)
        return p ** d

    squares = {pow(i, 2, p) for i in range(p)}
    final_set: set = set()

    for beta in range(p):
        beta_sq = (beta * beta) % p
        for s_tuple in itertools.product(squares, repeat=d - 1):
            point = tuple((s - beta_sq) % p for s in s_tuple) + (beta,)
            final_set.add(point)

    # Add the hyperplane F_p^(d-1) × {0}
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


# ---------------------------------------------------------------------------
# Public entry-point
# ---------------------------------------------------------------------------

def evaluate(output, p: int = 3, d: int = 3, **kwargs) -> dict:
    """Score a candidate Kakeya set construction.

    Parameters
    ----------
    output:
        Integer array of shape (k, d) with entries in {0, …, p-1}.
    p:
        Prime order of the finite field.
    d:
        Dimension of the vector space.

    Returns
    -------
    dict
        score   : -(|K| / reference_size); higher (less negative) is better.
        valid   : True iff the set is a valid Kakeya set.
        error   : description of the first error, or ''.
        metrics : dict with set_size, reference_size, is_kakeya.
    """
    try:
        try:
            construction = np.asarray(output, dtype=np.int64)
        except Exception as exc:
            return {"score": 0.0, "valid": False,
                    "error": f"Cannot convert output to array: {exc}",
                    "metrics": {}}

        if construction.ndim != 2 or construction.shape[1] != d:
            return {"score": 0.0, "valid": False,
                    "error": (f"Expected shape (k, {d}), "
                              f"got {construction.shape}"),
                    "metrics": {}}

        if construction.size == 0:
            return {"score": 0.0, "valid": False,
                    "error": "Empty construction", "metrics": {}}

        if np.any(construction < 0) or np.any(construction >= p):
            return {"score": 0.0, "valid": False,
                    "error": f"All entries must be in {{0, …, {p-1}}}",
                    "metrics": {}}

        # Deduplicate
        unique_pts = np.unique(construction, axis=0)
        k = unique_pts.shape[0]

        ref_size = _saraf_sudan_size(p, d)
        if ref_size == 0:
            return {"score": 0.0, "valid": False,
                    "error": "Reference size is 0 (invalid p or d)",
                    "metrics": {}}

        is_kakeya = _is_valid_kakeya(unique_pts, p, d)

        if not is_kakeya:
            return {
                "score": float(-1e6),
                "valid": False,
                "error": "Construction is not a valid Kakeya set",
                "metrics": {
                    "set_size": k,
                    "reference_size": ref_size,
                    "is_kakeya": False,
                },
            }

        score = -float(k) / float(ref_size)
        return {
            "score": score,
            "valid": True,
            "error": "",
            "metrics": {
                "set_size": k,
                "reference_size": ref_size,
                "normalized_score": score,
                "is_kakeya": True,
            },
        }

    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}
