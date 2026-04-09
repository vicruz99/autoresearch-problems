# Moving Sofa Problem (3D)

**Category:** geometry  
**Optimize:** Maximize `score`  
**Known best:** open

## Problem Statement

Find the path of 3D poses (translation + rotation) for moving a 3D solid through an L-shaped corridor of unit width. The solid shape is the intersection of the corridor at all poses. Score = approximate volume of the solid (computed by point sampling with n_grid=20).

n_poses=20 discrete poses parameterize the path.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `n_poses: 20`, `n_grid: 20` |

## Scoring

The evaluator estimates the intersection volume via a 20×20×20 grid. Higher volume is better.

## Known Results

- The 3D moving sofa problem is an open generalization of the 2D problem.
- The unit cube (not rotated) fits through the corridor with volume 1.
- Cylinders of diameter 1 and finite length provide better configurations.
- AlphaEvolve explored this as an open 3D geometry problem.

## Source

Google DeepMind / AlphaEvolve (Apache 2.0)
