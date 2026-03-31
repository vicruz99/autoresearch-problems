# Online Bin Packing Problem

## Task

Implement an **online bin-packing heuristic**.  Items with sizes drawn
uniformly from (0, 1] arrive one at a time.  Each item must be assigned
**immediately and irrevocably** to a bin of capacity 1.0 (you cannot
re-arrange items later).  The goal is to use as **few bins as possible**.

## What to implement

Implement a function `solve(item_size, bins)` that is called once per item:

```python
def solve(item_size: float, bins: list[float]) -> int:
    """
    Parameters
    ----------
    item_size : float
        Size of the current item, in (0, 1].
    bins : list[float]
        Remaining capacity of each currently open bin.

    Returns
    -------
    int
        Index into `bins` indicating which bin to place the item in,
        or -1 to open a new bin.
    """
    ...
```

## Scoring

- **Score = −(number of bins used)** across 100 random items with seed 42.
- A higher score is better (fewer bins → less negative score).
- Score = 0 if the heuristic places an item in a bin with insufficient capacity.

## Notes

- The **First Fit Decreasing** offline algorithm achieves near-optimal, but it requires seeing all items first.
- Online strategies like **Best Fit** (place in the fullest bin that still fits) or **First Fit** (place in the first bin that fits) are good baselines.
- Can you beat First Fit or Best Fit using a learned or adaptive policy?
