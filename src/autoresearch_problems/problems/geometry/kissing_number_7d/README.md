# Kissing Number in 7D

**Category:** geometry  
**Optimize:** Maximize `score`  
**Known best:** 126

## Problem Statement

Kissing number problem in dimension 7: find the maximum number of non-overlapping unit spheres that can simultaneously touch a central unit sphere in 7-dimensional space.

Score = count. Best known lower bound: 126. Upper bound: 134.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `dimension: 7` |

## Scoring

Count of valid kissing vectors (pairwise angle ≥ 60°).

## Known Results

- Lower bound: 126 (E₇ lattice).
- Upper bound: 134.
- AlphaEvolve matched the lower bound of 126.

## Source

[AlphaEvolve repository of problems](https://github.com/google-deepmind/alphaevolve_repository_of_problems)
