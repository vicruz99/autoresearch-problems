# Edges vs. Triangles

**Category:** combinatorics  
**Optimize:** Maximize `score`  
**Known best:** 1.0

## Problem Statement

Find a set of n=20 probability vectors (each of length 20) that densely traces the theoretical boundary of the achievable (edge_density, triangle_density) region for graphs.

Score = (5/6) / (area + 10 × max_gap), where:
- `area` is the area under the empirical curve (should approach 5/6 for the capped slope-3 boundary).
- `max_gap` is the largest gap between consecutive edge densities.

A score of 1.0 corresponds to the theoretical minimum area = 5/6 with zero gap — perfect coverage of the Kruskal-Katona boundary.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `n: 20` |

## Scoring

The evaluator interprets the 20×20 array as 20 probability vectors over graph structures, computes the implied (edge_density, triangle_density) curve, and scores coverage of the Kruskal-Katona boundary.

## Known Results

- The Kruskal-Katona theorem characterizes the achievable (edge, triangle) density region.
- Perfect score 1.0 is achievable in principle; AlphaEvolve found constructions achieving this.

## Source

[AlphaEvolve repository of problems](https://github.com/google-deepmind/alphaevolve_repository_of_problems)
