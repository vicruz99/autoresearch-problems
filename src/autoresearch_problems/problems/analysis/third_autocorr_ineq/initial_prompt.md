Act as an expert software developer and inequality specialist specializing in creating step functions with certain properties.

Your task is to generate the sequence of heights of a step function that minimizes the third autocorrelation constant C₃:

```python
def evaluate_sequence(sequence: np.ndarray) -> float:
    """Compute the C3 upper bound."""
    n = len(sequence)
    b = np.convolve(sequence, sequence)
    max_abs_b = float(np.max(np.abs(b)))
    sum_abs = float(np.sum(np.abs(sequence)))
    c3 = 2 * n * max_abs_b / sum_abs**2
    return c3
```

Your `solve()` function must return a list of floats (can be positive or negative).

Score = c3 directly (lower is better). AlphaEvolve achieved C₃ ≤ 1.4556427953745406.
Goal: Return a sequence with evaluate_sequence(sequence) < 1.4556427953745406.
