from typing import List


def solve() -> List[int]:
    """Return a list of non-negative integers forming a difference basis.

    A difference basis B covers all integers in {1, ..., k} if every such
    integer can be written as b_i - b_j for some b_i, b_j in B with b_i > b_j.

    The score is k / n² where n = |B|.  The theoretical maximum is ≈ 0.5.

    Returns
    -------
    List[int] of non-negative integers.
    """
    # EVOLVE-BLOCK-START
    # Trivial consecutive basis: {0, 1, ..., 9}
    # Covers 1..9 with n=10 elements → k/n² = 9/100 = 0.09  (poor).
    basis = list(range(10))
    # EVOLVE-BLOCK-END

    return basis
