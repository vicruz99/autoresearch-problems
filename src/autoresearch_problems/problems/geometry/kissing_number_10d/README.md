# Kissing Number in 10D

**Category:** geometry  
**Optimize:** Maximize `score`  
**Known best:** 500

## Problem Statement

Kissing number problem in dimension 10: find the maximum number of non-overlapping unit spheres that can simultaneously touch a central unit sphere in 10-dimensional space.

Score = count. Best known lower bound: 500 (matched by AlphaEvolve). Upper bound: 554.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `dimension: 10` |

## Scoring

Count of valid kissing vectors (pairwise angle ≥ 60°).

## Known Results

- Lower bound: 500 (improved by AlphaEvolve).
- Upper bound: 554 (LP bound).
- Previous lower bound: 336. AlphaEvolve dramatically improved to 500.

## Source

[AlphaEvolve repository of problems](https://github.com/google-deepmind/alphaevolve_repository_of_problems)
