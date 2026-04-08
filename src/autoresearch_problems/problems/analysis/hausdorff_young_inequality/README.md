# Hausdorff-Young Inequality

**Category:** analysis  
**Optimize:** Maximize `score`  
**Known best:** ≈ 0.9532

## Problem Statement

Find a function f (values on a grid of j=500 points over [−r1, r1] = [−5, 5]) that maximizes the Hausdorff-Young quotient:

    Q(f) = ‖f̂‖_{L^q} / ‖f‖_{L^p}

where p = 1.5, q = p/(p−1) = 3, and f̂ is the Fourier transform of f (extended to [−r2, r2] = [−10, 10]). Higher is better. The sharp constant is the Babenko-Beckner constant, achieved by Gaussians.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `p: 1.5`, `r1: 5.0`, `j: 500`, `r2: 10.0` |

## Scoring

The evaluator:
1. Computes the Fourier transform of f.
2. Returns Q(f) = ‖f̂‖_{L^q} / ‖f‖_{L^p} (higher is better; maximum ≈ 0.9532).

## Known Results

- Sharp constant (Babenko-Beckner): achieved by f(x) = exp(−πx²).
- AlphaEvolve confirmed Q ≈ 0.9532 for Gaussian input.
- Problem is essentially solved; use as calibration.

## Source

[AlphaEvolve repository of problems](https://github.com/google-deepmind/alphaevolve_repository_of_problems)
