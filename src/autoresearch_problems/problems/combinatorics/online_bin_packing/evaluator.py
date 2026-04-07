"""Evaluator for the Online Bin Packing problem.

The candidate provides a *heuristic function* that receives the current item
size and a list of remaining capacities of open bins, and returns the index
of the bin to place the item in (or -1 to open a new bin).

The evaluator simulates the online process on a random instance and returns
the negative number of bins used (so that maximising the score is equivalent
to minimising the number of bins).

This file is standalone and library-agnostic — it does NOT import from
autoresearch_problems.  The only dependency is numpy.
"""

#from __future__ import annotations

import numpy as np


def evaluate(
    output: object,
    num_items: int = 100,
    seed: int = 42,
    **kwargs,
) -> dict:
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
    dict
        ``score`` = ``-num_bins_used`` (higher is better; fewer bins is better).
        ``valid`` = True iff the heuristic successfully packed all items.
        ``error`` = description of the first error found, or empty string.
        ``metrics`` = dict with extra info (e.g. ``num_bins``, ``num_items``).
    """
    if not (isinstance(num_items, int) or (isinstance(num_items, float) and num_items == int(num_items))) or int(num_items) < 1:
        return {
            "score": 0.0,
            "valid": False,
            "error": f"num_items must be a positive integer >= 1, got num_items={num_items}",
            "metrics": {},
        }
    num_items = int(num_items)

    if not callable(output):
        return {
            "score": 0.0,
            "valid": False,
            "error": "output must be a callable with signature (item_size, bins) -> int",
            "metrics": {},
        }

    rng = np.random.default_rng(seed)
    items = rng.uniform(0.0, 1.0, size=num_items).tolist()

    bins: list[float] = []  # remaining capacity of each open bin
    BIN_CAPACITY = 1.0

    try:
        for item_size in items:
            if item_size > BIN_CAPACITY:
                return {
                    "score": 0.0,
                    "valid": False,
                    "error": f"Item size {item_size} exceeds bin capacity {BIN_CAPACITY}",
                    "metrics": {},
                }

            idx = output(item_size, list(bins))

            if idx == -1 or len(bins) == 0:
                bins.append(BIN_CAPACITY - item_size)
            else:
                if not isinstance(idx, int):
                    try:
                        idx = int(idx)
                    except (TypeError, ValueError):
                        return {
                            "score": 0.0,
                            "valid": False,
                            "error": f"Heuristic returned non-integer index: {idx!r}",
                            "metrics": {},
                        }
                if idx < 0 or idx >= len(bins):
                    return {
                        "score": 0.0,
                        "valid": False,
                        "error": f"Bin index {idx} out of range (num_bins={len(bins)})",
                        "metrics": {},
                    }
                if bins[idx] < item_size:
                    return {
                        "score": 0.0,
                        "valid": False,
                        "error": (
                            f"Item of size {item_size:.4f} does not fit in bin {idx} "
                            f"with remaining capacity {bins[idx]:.4f}"
                        ),
                        "metrics": {},
                    }
                bins[idx] -= item_size
    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}

    num_bins = len(bins)
    return {
        "score": float(-num_bins),
        "valid": True,
        "error": "",
        "metrics": {"num_bins": num_bins, "num_items": num_items},
    }
