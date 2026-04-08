# First Autocorrelation Inequality

**Category:** analysis  
**Optimize:** Minimize `score`  
**Known best:** C₁ ≤ 1.5053

## Problem Statement

Find a non-negative step function f on [−1/4, 1/4] (discretized into `num_intervals = 600` equal-width intervals) that minimizes the first autocorrelation constant:

    C₁ = max_{|t| ≤ 1/2} (f * f)(t) / (∫f)²

where `f * f` is the convolution of f with itself. Lower is better. This provides an upper bound on C₁ — the true minimum is an open problem. Previously C₁ ≤ 1.5098; AlphaEvolve improved to C₁ ≤ 1.5053. The theoretical lower bound is C₁ ≥ 1.28.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `list[float]` |
| Parameters | `num_intervals: 600` |

## Scoring

The evaluator:
1. Interprets the list as values of f on 600 uniform intervals over [−1/4, 1/4].
2. Computes the convolution f * f.
3. Returns C₁ = max_{|t| ≤ 1/2} (f * f)(t) / (∫f)² (lower is better).

## Known Results

- Lower bound: C₁ ≥ 1.28 (known).
- Previous best: C₁ ≤ 1.5098.
- AlphaEvolve: C₁ ≤ 1.5052939684401607.
- True optimum is open.

## Source

AlphaEvolve (Google DeepMind)
