# Moving Sofa Problem (2D)

**Category:** geometry  
**Optimize:** Maximize `score`  
**Known best:** open (Gerver's sofa ≈ 2.2195)

## Problem Statement

Find the path of poses (translations + rotations) for moving a 2D sofa around an L-shaped corridor of unit width. The sofa shape is the intersection of the corridor hallway at all poses along the path. Score = approximate area of the sofa (computed by point sampling with n_grid=50).

n_poses=20 discrete poses are used to parameterize the path.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `n_poses: 20`, `n_grid: 50` |

## Scoring

The evaluator:
1. Constructs the sofa as the intersection of corridor positions at all n_poses.
2. Approximates its area via a 50×50 grid.
3. Returns the estimated area (higher is better).

## Known Results

- Hammersley's sofa: area = π/2 + 2/π ≈ 2.2074.
- Gerver's sofa (conjectured optimal): area ≈ 2.2195.
- Romik's numerical optimal: area ≈ 2.2195.
- This is the famous "moving sofa problem" — exact optimum is open.

## Source

Google DeepMind / AlphaEvolve (Apache 2.0)
