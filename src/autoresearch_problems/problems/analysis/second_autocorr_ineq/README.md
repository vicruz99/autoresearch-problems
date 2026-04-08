# Second Autocorrelation Inequality

**Category:** analysis  
**Optimize:** Maximize `score`  
**Known best:** C₂ ≥ 0.8963

## Problem Statement

Find a non-negative step function f that maximizes the second autocorrelation constant:

    C₂ = ‖f * f‖₂² / (‖f * f‖₁ · ‖f * f‖∞)

where f * f is the autocorrelation (convolution of f with itself). Higher C₂ is better. This provides a lower bound — a larger C₂ means the autocorrelation function is "more uniform". AlphaEvolve achieved C₂ ≥ 0.8963.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `list` |
| Parameters | none (empty dict) |

## Scoring

The evaluator:
1. Interprets the list as values of f (non-negative step function).
2. Computes A = f * f (autocorrelation).
3. Returns C₂ = ‖A‖₂² / (‖A‖₁ · ‖A‖∞) (higher is better).

## Known Results

- AlphaEvolve achieved C₂ ≥ 0.8962799441554083.
- Upper bound: C₂ ≤ 1 (by Cauchy-Schwarz, with equality iff A is constant).
- True optimum is open.

## Source

AlphaEvolve (Google DeepMind)
