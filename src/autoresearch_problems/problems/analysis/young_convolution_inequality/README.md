# Young's Convolution Inequality

**Category:** analysis  
**Optimize:** Maximize `score`  
**Known best:** open

## Problem Statement

Find two functions f and g (each as values on j=500 uniform points over [−r1, r1] = [−10, 10]) that maximize Young's convolution quotient:

    Q(f, g) = ‖f * g‖_{L^r} / (‖f‖_{L^p} · ‖g‖_{L^q})

with p = 4/3, q = 7/5, and 1/r = 1/p + 1/q − 1. The sharp constant for Young's inequality is achieved by Gaussians.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `p: 4/3 ≈ 1.333`, `q: 7/5 = 1.4`, `r1: 10.0`, `j: 500` |

## Scoring

The evaluator:
1. Splits the returned array into two halves: f = output[:j] and g = output[j:].
2. Computes the convolution f * g.
3. Returns Q(f, g) (higher is better).

## Known Results

- Sharp constant for Young's inequality achieved by Gaussians (Beckner 1975).
- The exact best score depends on the specific (p, q) pair used.
- AlphaEvolve used this as a benchmark; exact optimum is open for this parameterization.

## Source

[AlphaEvolve repository of problems](https://github.com/google-deepmind/alphaevolve_repository_of_problems)
