# Kakeya Needle Problem (3D)

**Category:** geometry  
**Optimize:** Maximize `score` (minimize volume)  
**Known best:** open

## Problem Statement

Three-dimensional Kakeya needle problem. For cap_n=4, find positions (x_rand, y_rand) — each an array of N²=16 floats — such that the union of N²=16 generalized tubes in [0,1]³ has minimum volume.

Tube (i,j) connects a 1/N × 1/N square at z=0 with base (x[i·N+j], y[i·N+j]) to a 1/N × 1/N square at z=1 offset by (i/N, j/N).

Score = −(volume / reference_volume); higher is better.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `list` |
| Parameters | `cap_n: 4`, `num_samples: 200000` |

## Scoring

The evaluator:
1. Uses Monte Carlo sampling (200,000 points) to estimate the union volume.
2. Returns score = −volume / reference_volume.

## Known Results

- The 3D Kakeya conjecture (that Kakeya sets have full Hausdorff dimension) is open.
- Discrete tube constructions provide lower bounds on the minimum volume.
- AlphaEvolve explored this as a discrete geometry optimization.

## Source

[AlphaEvolve repository of problems](https://github.com/google-deepmind/alphaevolve_repository_of_problems)
