# Gagliardo-Nirenberg Inequality

**Category:** analysis  
**Optimize:** Maximize `score`  
**Known best:** ≈ 0.1111 (= 1/9)

## Problem Statement

Find a function f (represented as values on a grid of j=500 points over [−r1, r1] = [−15, 15]) that maximizes the Gagliardo-Nirenberg quotient:

    Q(f) = ‖f‖_p^{4p} / (‖f‖_2^{2(p+2)} · ‖f'‖_2^{2(p−2)})

with p = 4. Higher is better. The known optimal function is f = sech(x) = 1/cosh(x), which achieves Q = 1/9 ≈ 0.1111 exactly.

The Gagliardo-Nirenberg inequality states Q(f) ≤ C for all f, and finding the sharp constant C = 1/9 is achieved by the sech function.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `p: 4.0`, `r1: 15.0`, `j: 500` |

## Scoring

The evaluator:
1. Interprets the array as values of f on 500 points over [−15, 15].
2. Computes ‖f‖_p, ‖f‖_2, and ‖f'‖_2 numerically.
3. Returns Q(f) (higher is better; maximum possible ≈ 0.1111).

## Known Results

- Optimal function: f(x) = sech(x) = 1/cosh(x) (up to scaling and translation).
- Sharp constant: Q = 1/9 ≈ 0.1111.
- The problem is essentially solved; use this as a calibration benchmark.

## Source

[AlphaEvolve repository of problems](https://github.com/google-deepmind/alphaevolve_repository_of_problems)
