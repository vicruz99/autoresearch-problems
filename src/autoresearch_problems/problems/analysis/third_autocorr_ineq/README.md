# Third Autocorrelation Inequality

**Category:** analysis  
**Optimize:** Minimize `score`  
**Known best:** C₃ ≤ 1.4556

## Problem Statement

Find a step function f on [−1/4, 1/4] (values may be negative) that minimizes the third autocorrelation constant:

    C₃ = 2n · max|f * f| / (Σ|f|)²

where f * f is the convolution of f with itself, and n is the number of intervals. Lower is better. AlphaEvolve achieved C₃ ≤ 1.4556.

This provides an upper bound on C₃ — the true minimum is an open problem. Unlike C₁ and C₂, the function f may take negative values.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `list` |
| Parameters | none (empty dict) |

## Scoring

The evaluator:
1. Interprets the list as values of f on uniform intervals over [−1/4, 1/4].
2. Computes the convolution f * f.
3. Returns C₃ = 2n · max|f * f| / (Σ|f|)² (lower is better).

## Known Results

- AlphaEvolve achieved C₃ ≤ 1.4556427953745406.
- Previous best: C₃ ≤ 1.5 (known classical bound).
- True optimum is open.

## Source

AlphaEvolve (Google DeepMind)
