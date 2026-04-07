"""Naive uniform seed solution for the First Autocorrelation Inequality problem."""


def solve(num_intervals: int = 600, **kwargs) -> list:
    """Return a uniform step function on num_intervals equally-spaced intervals.

    This is the simplest possible baseline: f(x) = 1 everywhere on [-1/4, 1/4].
    The resulting C₁ ratio is the starting point for the LLM to improve upon.
    """
    num_intervals = int(num_intervals)
    return [1.0] * num_intervals
