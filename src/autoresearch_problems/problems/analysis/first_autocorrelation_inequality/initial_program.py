"""Naive uniform seed solution for the First Autocorrelation Inequality problem."""


def solve() -> list[float]:
    """Return a uniform step function on 600 equally-spaced intervals.

    This is the simplest possible baseline: f(x) = 1 everywhere on [-1/4, 1/4].
    The resulting C₁ ratio is the starting point for the LLM to improve upon.
    """
    num_intervals = 600
    return [1.0] * num_intervals
