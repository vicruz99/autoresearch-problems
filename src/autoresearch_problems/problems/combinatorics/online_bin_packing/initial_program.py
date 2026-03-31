"""First Fit seed solution for the Online Bin Packing problem."""


def solve(item_size: float, bins: list[float]) -> int:
    """First Fit heuristic: place the item in the first bin that fits."""
    for i, remaining in enumerate(bins):
        if remaining >= item_size:
            return i
    return -1  # open a new bin
