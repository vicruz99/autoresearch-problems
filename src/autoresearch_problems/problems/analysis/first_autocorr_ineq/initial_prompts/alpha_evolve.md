Act as an expert software developer and inequality specialist specializing in creating step functions with certain properties.

Your task is to generate the sequence of non-negative heights of a step function, that minimizes the following evaluation function:

```python
def evaluate_sequence(sequence: list[float]) -> float:
    n = len(sequence)
    b_sequence = np.convolve(sequence, sequence)
    max_b = max(b_sequence)
    sum_a = np.sum(sequence)
    return float(2 * n * max_b / (sum_a**2))
```

Your task is to write a `solve()` function that searches for the best sequence of coefficients. Your function should return within 55 seconds with the best sequence it found. All numbers in your sequence have to be positive or zero.

You may code up any search method you want.

BENCHMARK: The current best known upper bound is C₁ ≤ 1.5052939684401607 (found by AlphaEvolve).
Goal: Return a sequence with evaluate_sequence(sequence) < 1.5052939684401607.
