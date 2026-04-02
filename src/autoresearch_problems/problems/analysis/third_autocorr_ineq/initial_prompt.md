Act as an expert software developer and inequality specialist specializing in creating step functions with certain properties.

Your task is to generate the sequence of heights of a step function that minimizes the following evaluation function:

```python
def evaluate_sequence(sequence: np.ndarray) -> float:
    """Compute the C3 upper bound."""
    conv = np.convolve(sequence, sequence, mode="full")
    n = len(sequence)
    max_conv_abs = float(np.max(conv))
    sum_heights = float(np.sum(sequence))
    sum_squared = sum_heights ** 2
    c3 = abs(2 * n * max_conv_abs / sum_squared)
    return c3
```

Your `solve()` function must return a list of floats (can be positive or negative).

BENCHMARK: The current best known upper bound is C₃ ≤ 1.4556427953745406 (found by AlphaEvolve).
Goal: Return a sequence with evaluate_sequence(sequence) < 1.4556427953745406.
