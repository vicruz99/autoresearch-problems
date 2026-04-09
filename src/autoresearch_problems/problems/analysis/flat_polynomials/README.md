# Flat Polynomials

**Category:** analysis  
**Optimize:** Minimize `score`  
**Known best:** ≈ 1.384 (n=64)

## Problem Statement

Find n = 64 coefficients c_i ∈ {+1, −1} for the polynomial

    g(z) = c_1·z + c_2·z² + … + c_n·z^n

that minimizes the L∞ norm on the unit circle, scaled by √(n+1):

    score = max_{|z|=1} |g(z)| / √(n+1)

This is related to Golay's conjecture on "flat" (low crest-factor) polynomials with ±1 coefficients. The theoretical minimum is conjectured to be 1 (a perfectly flat polynomial), but no such polynomial is known for large n. AlphaEvolve achieved ≈ 1.384 for n=64.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `n: 64` |

## Scoring

The evaluator:
1. Interprets the array as n coefficients; clips each to sign (±1).
2. Evaluates the polynomial on a dense grid of points on the unit circle.
3. Returns score = max|g(z)| / √(n+1) (lower is better).

## Known Results

- Golay (1961) conjectured flat polynomials exist; none found for large n.
- AlphaEvolve found score ≈ 1.3842203538985842 for n=64.
- Problem is related to the Rudin-Shapiro polynomials (score ≈ √2 ≈ 1.414).

## Source

[AlphaEvolve repository of problems](https://github.com/google-deepmind/alphaevolve_repository_of_problems)
