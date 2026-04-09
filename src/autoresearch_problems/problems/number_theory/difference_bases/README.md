# Difference Bases

**Category:** number_theory  
**Optimize:** Maximize `score`  
**Known best:** ≤ 0.5

## Problem Statement

Find a small set B of non-negative integers (a difference basis) such that every positive integer up to k can be expressed as a difference b_i − b_j for some b_i, b_j ∈ B.

Score = k / n², where n = |B| and k is the maximum consecutively covered integer. Maximize this ratio. The theoretical bound gives k/n² ≤ 0.5 asymptotically.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `list[int]` |
| Parameters | none |

## Scoring

The evaluator:
1. Takes the list as a set B of non-negative integers.
2. Computes k = maximum integer covered consecutively starting from 1.
3. Returns score = k / |B|².

## Known Results

- Theoretical upper bound: k/n² ≤ 0.5 (equivalent to δ[k]² ≤ 2/k).
- Known constructions approach ratio 0.5 for large n.
- AlphaEvolve found constructions achieving known_best_score = 0.5.
- Related to the Erdős–Turán conjecture on additive bases.

## Source

[AlphaEvolve repository of problems](https://github.com/google-deepmind/alphaevolve_repository_of_problems)
