Act as an expert software developer and inequality specialist specializing in creating step functions with certain properties.

Your task is to generate the sequence of non-negative heights of a step function that maximizes the second autocorrelation constant C₂:

```python
def evaluate_sequence(heights_sequence):
    b = np.convolve(heights_sequence, heights_sequence)
    c2 = np.sum(b**2) / (np.sum(b) * np.max(b))
    return c2
```

Your `solve()` function must return a list of non-negative floats.

Score = c2 directly (higher is better). AlphaEvolve achieved C₂ ≥ 0.8963.
Goal: Return a sequence with evaluate_sequence(sequence) > 0.8962799441554083.
