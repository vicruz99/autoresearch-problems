# Flat Polynomials and Golay's Conjecture

Act as a research mathematician and optimization specialist.

## Goal

For a given natural number `n`, find a one-dimensional Python list consisting
of `n` coefficients `c_i` (each one being either `+1` or `-1`) for
`i = 1, …, n` such that the polynomial

    g(z) = c_1·z + c_2·z² + … + c_n·z^n

minimises the quantity:

    max_{|z|=1} |g(z)| / √(n+1)

where the maximum is taken over the unit circle.

## Function Signature

```python
def solve(n: int = 64) -> list[float] | np.ndarray:
    """Return n coefficients in {+1, -1} minimising max|g(z)|/√(n+1)."""
```

## Evaluation

Your list of coefficients is scored by a function that computes
`max_{|z|=1} |g(z)| / √(n+1)` by sampling 100 000 equally-spaced points on
the unit circle.

**You want the score to be as small as possible (minimize).**

A score below 1.4 is challenging. AlphaEvolve achieved ~1.384 for `n = 64`.
Golay's conjecture (still open) predicts the minimum approaches 1 for
infinitely many `n`.

## Hints

- A pure all-ones sequence gives a score ≈ √n / √(n+1) ≈ 1 for large n, but
  that is typically not optimal.
- Random ±1 sequences give scores around 1.5–2.0.
- Suffix-flip hill climbing (flipping `c_k, c_{k+1}, …, c_n` for a random
  `k`) is a good baseline search.
- You may call the scoring function as many times as you wish inside `solve()`.
- You have `1000` seconds to run; use a `while time.time() - start_time < 990`
  loop.

## Initial Implementation

```python
import time
import numpy as np

def _c_plus_score(coefficients):
    n = len(coefficients)
    zs = np.exp(1j * np.linspace(0, 2 * np.pi, 100_000, endpoint=False))
    poly_coeffs = np.concatenate([coefficients[::-1], [0.0]])
    vals = np.polyval(poly_coeffs, zs)
    return float(np.max(np.abs(vals))) / np.sqrt(n + 1)

def solve(n: int = 64) -> np.ndarray:
    best_coefficients = np.ones(n)
    curr_coefficients = best_coefficients.copy()
    best_score = _c_plus_score(best_coefficients)
    start_time = time.time()
    while time.time() - start_time < 55:
        random_index = np.random.randint(0, n)
        curr_coefficients[random_index:] *= -1
        curr_score = _c_plus_score(curr_coefficients)
        if curr_score < best_score:
            best_score = curr_score
            best_coefficients = curr_coefficients.copy()
    return best_coefficients
```
