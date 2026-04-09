# Kakeya Needle Problem (2D)

**Category:** geometry  
**Optimize:** Maximize `score` (minimize area)  
**Known best:** open

## Problem Statement

Two-dimensional Kakeya needle problem. Find positions x = (x₁, ..., x_n) (with n=32) such that the union of n triangles R_i (with vertices (x_i, 0), (x_i + 1/n, 0), (x_i + i/n, 1)) has minimum area.

This is a discretized version of the Kakeya needle problem — finding the minimum area set in which a unit needle can be rotated 180°.

Score = −(area / reference_area), where reference is the Keich construction area. Higher (less negative) is better — a better construction beats the reference.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `n: 32` |

## Scoring

The evaluator:
1. Interprets the array as n x-offsets for triangle bases.
2. Computes the union area using Shapely.
3. Returns score = −area / reference_area.

## Known Results

- The Kakeya conjecture (solved in 2D) states the minimum area is 0 (Besicovitch, 1928).
- For discrete approximations, the Keich construction gives a good reference.
- AlphaEvolve explored improved discrete constructions.

## Source

[AlphaEvolve repository of problems](https://github.com/google-deepmind/alphaevolve_repository_of_problems)
