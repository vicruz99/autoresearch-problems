# Spherical t-Design (n=24, t=7)

**Category:** geometry  
**Optimize:** Maximize `score`  
**Known best:** open

## Problem Statement

Construct a spherical 7-design with n=24 points on the unit sphere in R³: a set of points such that the average of any polynomial of degree ≤ 7 over the points equals its average over the whole sphere.

Score = −max_error, where the error is measured across all Gegenbauer polynomials up to degree t=7. Higher (less negative) is better.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `n: 24`, `t: 7` |

## Scoring

The evaluator:
1. Normalizes points to the unit sphere.
2. For each Gegenbauer polynomial of degree k = 1, ..., 7, computes the average over points vs. exact value.
3. Returns score = −max_error.

## Known Results

- Spherical t-designs with minimal n are known up to moderate t.
- For t=7 in 3D, the minimum n is 12 (proved). With n=24, a perfect design (score 0) should exist.
- AlphaEvolve explored this as a numerical optimization problem.

## Source

Google DeepMind / AlphaEvolve (Apache 2.0)
