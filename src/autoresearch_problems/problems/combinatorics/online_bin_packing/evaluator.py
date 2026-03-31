"""Evaluator for the Online Bin Packing problem.

The candidate provides a *heuristic function* ``solve(item_size, bins)``
that receives the current item size and a list of remaining capacities of
open bins, and returns the index of the bin to place the item in (or -1 to
open a new bin).

The evaluator simulates the online process on a random instance and returns
the negative number of bins used (so that maximising the score is equivalent
to minimising the number of bins).
"""

from __future__ import annotations

from typing import Callable

import numpy as np

from autoresearch_problems.core.result import EvalResult


def evaluate(
    output: Callable[[float, list[float]], int],
    *,
    num_items: int = 100,
    seed: int = 42,
) -> EvalResult:
    """Score a candidate online bin-packing heuristic.

    Parameters
    ----------
    output:
        A callable with signature ``(item_size: float, bins: list[float]) -> int``
        where *bins* is a list of remaining capacities of open bins and the
        return value is an index into *bins* (place item there) or -1 (open a
        new bin).
    num_items:
        Number of items in the simulation.
    seed:
        Random seed for reproducibility.

    Returns
    -------
    EvalResult
        ``score`` = ``-num_bins_used`` (higher is better; fewer bins is better).
        ``valid`` = True iff the heuristic successfully packed all items.
    """
    if not callable(output):
        return EvalResult(
            score=0.0,
            valid=False,
            error="output must be a callable with signature (item_size, bins) -> int",
        )

    rng = np.random.default_rng(seed)
    items = rng.uniform(0.0, 1.0, size=num_items).tolist()

    bins: list[float] = []  # remaining capacity of each open bin
    BIN_CAPACITY = 1.0

    try:
        for item_size in items:
            if item_size > BIN_CAPACITY:
                return EvalResult(
                    score=0.0,
                    valid=False,
                    error=f"Item size {item_size} exceeds bin capacity {BIN_CAPACITY}",
                )

            idx = output(item_size, list(bins))

            if idx == -1 or len(bins) == 0:
                bins.append(BIN_CAPACITY - item_size)
            else:
                if not isinstance(idx, int):
                    try:
                        idx = int(idx)
                    except (TypeError, ValueError):
                        return EvalResult(
                            score=0.0,
                            valid=False,
                            error=f"Heuristic returned non-integer index: {idx!r}",
                        )
                if idx < 0 or idx >= len(bins):
                    return EvalResult(
                        score=0.0,
                        valid=False,
                        error=f"Bin index {idx} out of range (num_bins={len(bins)})",
                    )
                if bins[idx] < item_size:
                    return EvalResult(
                        score=0.0,
                        valid=False,
                        error=(
                            f"Item of size {item_size:.4f} does not fit in bin {idx} "
                            f"with remaining capacity {bins[idx]:.4f}"
                        ),
                    )
                bins[idx] -= item_size
    except Exception as exc:
        return EvalResult(score=0.0, valid=False, error=str(exc))

    num_bins = len(bins)
    return EvalResult(
        score=float(-num_bins),
        valid=True,
        metrics={"num_bins": num_bins, "num_items": num_items},
    )
