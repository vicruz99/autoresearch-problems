# Kissing Number in 6D

**Category:** geometry  
**Optimize:** Maximize `score`  
**Known best:** 72

## Problem Statement

Kissing number problem in dimension 6: find the maximum number of non-overlapping unit spheres that can simultaneously touch a central unit sphere in 6-dimensional space.

Score = count. Best known lower bound: 72. Upper bound: 78.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `dimension: 6` |

## Scoring

Count of valid kissing vectors (pairwise angle ≥ 60°).

## Known Results

- Lower bound: 72 (E₆ lattice).
- Upper bound: 78.
- AlphaEvolve matched the lower bound of 72.

## Source

[AlphaEvolve repository of problems](https://github.com/google-deepmind/alphaevolve_repository_of_problems)
