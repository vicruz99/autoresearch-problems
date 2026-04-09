# Kissing Cylinders

**Category:** geometry  
**Optimize:** Maximize `score`  
**Known best:** 0.0

## Problem Statement

Find 7 unit-radius infinite cylinders that all simultaneously touch a central cylinder aligned with the Z-axis. Each outer cylinder is defined by its axis direction and position. Score = −Σ(dist_i − 2)² for the 7 outer cylinders, where dist_i is the axis-to-axis distance between outer cylinder i and the central cylinder.

Score = 0 means all 7 cylinders are exactly tangent to the central one. Higher (less negative) is better.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `n_cylinders: 7` |

## Scoring

The evaluator:
1. Computes the axis-to-axis distance between each outer cylinder and the central Z-axis cylinder.
2. Returns score = −Σ(dist_i − 2)².

## Known Results

- The maximum number of unit cylinders that can simultaneously touch a central unit cylinder is an open problem.
- The known lower bound is 7 (AlphaEvolve's construction achieves all 7 tangent, score = 0).
- Higher kissing numbers for cylinders are unknown.

## Source

Google DeepMind / AlphaEvolve (Apache 2.0)
