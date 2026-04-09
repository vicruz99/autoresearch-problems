# Agent Guide — Prime Number Theorem

## Goal

Return a Python `dict` mapping positive integers k to real values f(k) such that Σ f(k)·⌊x/k⌋ ≤ 1 for all x ≥ 1, maximizing a_value = −Σ f(k)·log(k)/k.

## Strategy hints

- Think of f(k) as weights for a Dirichlet convolution approach to bounding ψ(x).
- The Möbius function μ provides a natural starting point: f(k) = μ(k)/k gives the prime indicator.
- Try f supported on small values (k ≤ 20) — the constraint is enforced for 100K samples.
- Non-negative f(k) = μ²(k)/φ(k) may satisfy the constraint easily.
- Linear programming: maximize a_value subject to the linear constraint matrix (k ≤ some_bound).
- Start with f = {1: 1} (identity) which gives a_value = 0 and check that the constraint holds.

## Output format

Return a Python `dict` mapping integer keys (k ≥ 1) to float values f(k).

```python
def solve(num_samples: int = 100000) -> dict:
    # Minimal example: f = {1: 1} (trivially satisfies constraint since floor(x/1) = x but need sum <= 1)
    # Better: f supported on primes with specific weights
    return {1: 0.5, 2: 0.1, 3: 0.05}
```

## Pitfalls

- If the constraint Σ f(k)·⌊x/k⌋ ≤ 1 is violated for any x, the result is invalid.
- The constraint is checked for 100K random x values — may miss edge cases.
- Negative f(k) values may help the objective but risk violating constraints for large x.

## Baseline

f = {1: 1/x_max} for some small x_max gives a tiny but valid a_value. The Möbius-based approach is more principled.
