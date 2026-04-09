# Prime Number Theorem

**Category:** number_theory  
**Optimize:** Maximize `score`  
**Known best:** open

## Problem Statement

Find a partial function f: Z⁺ → R (represented as a dict mapping positive integers to reals) that maximizes:

    a_value = −Σ f(k) · log(k) / k

subject to the constraint that for all x ≥ 1:

    Σ_{k} f(k) · ⌊x/k⌋ ≤ 1

This is related to finding optimal weights for the prime number theorem: the constraint says the "Chebyshev sum" Σ f(k) ψ(x/k) is bounded, and the score measures the rate of the resulting bound.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `dict` |
| Parameters | `num_samples: 100000` |

## Scoring

The evaluator:
1. Checks the constraint for num_samples=100000 random values of x.
2. Returns a_value = −Σ f(k) log(k)/k if all constraints are satisfied.

## Known Results

- The prime number theorem states ψ(x) ~ x (where ψ is the Chebyshev function).
- AlphaEvolve explored this as an optimization problem related to explicit PNT constants.
- Exact optimum is open; the problem is connected to zero-free regions of the Riemann zeta function.

## Source

Google DeepMind / AlphaEvolve (Apache 2.0)
