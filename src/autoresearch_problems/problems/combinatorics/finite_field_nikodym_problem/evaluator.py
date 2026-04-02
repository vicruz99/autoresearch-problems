# Adapted from google-deepmind/alphaevolve_repository_of_problems (Apache 2.0)
"""Evaluator for the Finite Field Nikodym Problem in F_q^2, q = p^2.

The candidate's solve() function must return a NumPy integer array of shape
(k, 2, 2) representing k points in F_q^2.  Each point is encoded as

    [[x_a, x_b], [y_a, y_b]]

where the first coordinate x = x_a + x_b*alpha and second y = y_a + y_b*alpha
are elements of F_q = F_{p^2}.  Here alpha is a root of x^2 - w over F_p,
and w is the smallest quadratic non-residue mod p.

The set N must be a valid Nikodym set: for every point x in F_q^2 there must
exist a non-zero direction v in F_q^2 such that the punctured line
    { x + t*v : t in F_q, t != 0 }
is entirely contained in N.

Score = |F_q^2| - |N|.  Higher is better (more points excluded).

This file is standalone — it does NOT import from autoresearch_problems.
"""

import numpy as np

_DEFAULT_P = 5
_DEFAULT_D = 2


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
    """Return True if construction_set is a valid Nikodym set in F_q^2.

    Uses the canonical direction representatives:
      - (1, m) for each m in F_q   → q directions
      - (0, 1)                     → 1 direction
    Each element of F_q is an index a*p + b.
    A point in F_q^2 is a tuple (idx1, idx2) of two F_q indices.
    """
    q = p * p
    # Build all non-zero t values (all q-1 elements t ≠ 0)
    nonzero_ts = [t for t in range(q) if t != 0]

    # idx_one = element 1 in F_q = index 1*p + 0 = p (for p > 1, otherwise 1)
    # Actually element 1 = (1, 0) = index 1*p + 0 = p ... no
    # (a, b) means a + b*alpha, so (1, 0) → index 1*p + 0 = p if p=5 then index 5
    # But (0, 1) → index 0*p + 1 = 1
    # Wait: index = a*p + b. Element 1 = (a=1, b=0) → index 1*p + 0 = p
    # Hmm but for p=5 that's index 5. Let me be careful.
    # Element zero = (0,0) → index 0
    # Element one = (1,0) → index p
    idx_zero = 0          # (0, 0)
    idx_one = 1 * p + 0  # (1, 0)

    for x1 in range(q):
        for x2 in range(q):
            found = False
            # Directions (v1=1, v2=m) for m in F_q
            for m in range(q):
                # Check all t ≠ 0 in F_q: is x + t*(1, m) in N?
                all_in = True
                for t in nonzero_ts:
                    # t*(1,0) = (t,0)? No: t*(1,m) = (t*1, t*m) in F_q
                    # Actually v1=idx_one, v2=m. t*v1 = mul[t, idx_one], t*v2 = mul[t, m]
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
            # Direction (v1=0, v2=1)
            all_in = True
            for t in nonzero_ts:
                tv2 = mul_table[t, idx_one]
                # v1=0 → t*v1=0, v2=idx_one → t*v2 = mul[t, idx_one]
                p1 = x1  # add 0
                p2 = add_table[x2, tv2]
                if (p1, p2) not in construction_set:
                    all_in = False
                    break
            if all_in:
                found = True
            if not found:
                return False
    return True


# ---------------------------------------------------------------------------
# Public evaluate interface
# ---------------------------------------------------------------------------

def evaluate(output, p: int = _DEFAULT_P, d: int = _DEFAULT_D, **kwargs) -> dict:
    """Score a candidate Nikodym set.

    Parameters
    ----------
    output:
        Integer array of shape (k, 2, 2) with values in {0, …, p-1}.
        Each row [[xa,xb],[ya,yb]] represents a point in F_{p^2}^2.
    p:
        Prime defining F_q with q = p^2.
    d:
        Dimension (must be 2).

    Returns
    -------
    dict
        score   : |F_q^2| − |N|  – **higher is better**
        valid   : True iff N is a valid Nikodym set with correct format
        error   : "" on success, description of first problem otherwise
        metrics : dict with nikodym_set_size, complement_size, total_space
    """
    try:
        q = p * p
        total = q ** d  # = q^2 for d=2

        try:
            arr = np.asarray(output, dtype=np.int64)
        except Exception as exc:
            return {"score": 0, "valid": False, "error": f"Cannot convert to array: {exc}", "metrics": {}}

        if d != 2:
            return {"score": 0, "valid": False, "error": "Only d=2 is supported", "metrics": {}}

        if arr.ndim != 3 or arr.shape[1] != 2 or arr.shape[2] != 2:
            return {
                "score": 0,
                "valid": False,
                "error": f"Expected shape (k,2,2), got {arr.shape}",
                "metrics": {},
            }

        if arr.size > 0 and (arr.min() < 0 or arr.max() >= p):
            return {
                "score": 0,
                "valid": False,
                "error": f"Array values must be in {{0, …, {p-1}}}",
                "metrics": {},
            }

        # De-duplicate and convert to set of tuples
        unique_set: set = set()
        for row in arr:
            pt = (int(row[0, 0]) * p + int(row[0, 1]),
                  int(row[1, 0]) * p + int(row[1, 1]))
            unique_set.add(pt)

        k = len(unique_set)

        add_table, mul_table, _ = _get_tables(p)

        is_valid = _is_valid_nikodym(unique_set, p, add_table, mul_table)

        if not is_valid:
            return {
                "score": 0,
                "valid": False,
                "error": "Not a valid Nikodym set",
                "metrics": {"nikodym_set_size": k, "complement_size": 0, "total_space": total},
            }

        complement = total - k
        return {
            "score": complement,
            "valid": True,
            "error": "",
            "metrics": {
                "nikodym_set_size": k,
                "complement_size": complement,
                "total_space": total,
            },
        }

    except Exception as exc:
        return {"score": 0, "valid": False, "error": f"Unexpected error: {exc}", "metrics": {}}
