# Agent Guide — Online Bin Packing

## Goal

Return a heuristic function that assigns each item to a bin online; minimize number of bins used for 100 items with seed=42; maximize score = −bins.

## Strategy hints

- Your `solve()` must **return a function**, not a number or array.
- Implement Best Fit Decreasing adapted for online: assign to the bin with the least remaining capacity that still fits.
- Score-based heuristics that track remaining capacity per bin outperform simple First Fit.
- Consider adding look-ahead or grouping logic based on item size ranges.
- The test uses a fixed random seed — you can potentially tune to that specific sequence, but generalizable heuristics are preferred.

## Output format

`solve()` must return a callable `heuristic(item_size: float, bins: list[float]) -> int` where `bins[i]` is the remaining capacity of bin i, and the return value is the bin index to use (or len(bins) to open a new bin).

```python
def solve(num_items: int = 100, seed: int = 42):
    def heuristic(item_size: float, bins: list) -> int:
        # Best Fit: find bin with least remaining space that fits
        best_idx = -1
        best_remaining = float('inf')
        for i, remaining in enumerate(bins):
            if remaining >= item_size and remaining - item_size < best_remaining:
                best_remaining = remaining - item_size
                best_idx = i
        if best_idx == -1:
            return len(bins)  # open new bin
        return best_idx
    return heuristic
```

## Pitfalls

- Returning a value instead of a function will cause the evaluator to fail immediately.
- The function signature must accept `(item_size, bins)` in that order.
- Assigning to a bin with insufficient remaining capacity is invalid.

## Baseline

First Fit (assign to first bin that fits) uses ~55 bins for 100 items. Best Fit uses ~52 bins. Perfect packing would use ~50 bins.
