# Kissing Number in 11D

**Category:** geometry  
**Optimize:** Maximize `score`  
**Known best:** 593

## Problem Statement

Kissing number problem in dimension 11: find the maximum number of non-overlapping unit spheres that can simultaneously touch a central unit sphere in 11-dimensional space.

Score = count. AlphaEvolve improved the lower bound from 592 to 593.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `dimension: 11` |

## Scoring

Count of valid kissing vectors (pairwise angle ≥ 60°).

## Known Results

- Previous lower bound: 592.
- AlphaEvolve new lower bound: 593.
- Upper bound: unknown (not in LP-provable range).
- This was a state-of-the-art improvement as of 2025.

## Source

[AlphaEvolve repository of problems](https://github.com/google-deepmind/alphaevolve_repository_of_problems)
