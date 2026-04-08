# Packing Circles — Maximum Sum of Radii

**Category:** geometry  
**Optimize:** Maximize `score`  
**Known best:** open

## Problem Statement

Pack n=26 non-overlapping circles of possibly different radii inside the unit square [0,1]². Maximize the sum of radii.

Score = sum of radii (higher is better).

Unlike uniform circle packing, here circles can have different sizes — use one large circle and many small ones, or find a balanced arrangement.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `n: 26` |

## Scoring

The evaluator:
1. Checks that all circles are inside [0,1]² (center ± radius within bounds).
2. Checks that no two circles overlap (distance between centers ≥ r_i + r_j).
3. Returns score = Σ r_i.

## Known Results

- Optimal packing of circles with varying radii in a square is an open problem.
- A single circle of radius 0.5 gives score 0.5.
- Using 26 smaller circles of equal radius ≈ 0.089 gives score ≈ 26 × 0.089 ≈ 2.3.

## Source

Google DeepMind / AlphaEvolve (Apache 2.0)
