# Kissing Number in 5D

**Category:** geometry  
**Optimize:** Maximize `score`  
**Known best:** 40

## Problem Statement

Kissing number problem in dimension 5: find the maximum number of non-overlapping unit spheres that can simultaneously touch a central unit sphere in 5-dimensional space.

Score = count of valid kissing vectors. Best known lower bound: 40 (matched by AlphaEvolve). Upper bound: 44.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `dimension: 5` |

## Scoring

The evaluator normalizes vectors and counts how many mutually satisfy the kissing condition (pairwise angle ≥ 60°).

## Known Results

- Lower bound: 40 (known construction).
- Upper bound: 44 (Kabatiansky-Levenshtein).
- AlphaEvolve matched the lower bound of 40.
- True K(5) ∈ {40, 41, 42, 43, 44}.

## Source

[AlphaEvolve repository of problems](https://github.com/google-deepmind/alphaevolve_repository_of_problems)
