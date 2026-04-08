# Kissing Number in 3D

**Category:** geometry  
**Optimize:** Maximize `score`  
**Known best:** 12

## Problem Statement

Kissing number problem in dimension 3: find the maximum number of non-overlapping unit spheres that can simultaneously touch a central unit sphere in 3-dimensional space.

Equivalently, find a set C ⊂ R³ with vectors of equal length, such that the minimum pairwise distance is at least as large as the maximum vector length.

Score = |C| (number of vectors). K(3) = 12 is proved.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `dimension: 3` |

## Scoring

The evaluator:
1. Normalizes all vectors to the unit sphere.
2. Checks that min pairwise distance ≥ max vector length (all kissing).
3. Returns score = number of valid vectors.

## Known Results

- K(3) = 12 was proved by Schütte and van der Waerden in 1953.
- Optimal configurations: icosahedral arrangement.
- This problem is pedagogical/solved — use as a sanity check.

## Source

[AlphaEvolve repository of problems](https://github.com/google-deepmind/alphaevolve_repository_of_problems)
