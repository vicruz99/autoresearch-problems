# Kissing Number in 9D

**Category:** geometry  
**Optimize:** Maximize `score`  
**Known best:** 306

## Problem Statement

Kissing number problem in dimension 9: find the maximum number of non-overlapping unit spheres that can simultaneously touch a central unit sphere in 9-dimensional space.

Score = count. Best known lower bound: 306. Upper bound: 364.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `dimension: 9` |

## Scoring

Count of valid kissing vectors (pairwise angle ≥ 60°).

## Known Results

- Lower bound: 306 (lattice construction).
- Upper bound: 364 (LP bound).
- AlphaEvolve matched the lower bound of 306.
- True K(9) ∈ {306, ..., 364}.

## Source

[AlphaEvolve repository of problems](https://github.com/google-deepmind/alphaevolve_repository_of_problems)
