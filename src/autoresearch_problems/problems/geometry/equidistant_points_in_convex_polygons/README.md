# Equidistant Points in Convex Polygons

**Category:** geometry  
**Optimize:** Maximize `score`  
**Known best:** 1.0

## Problem Statement

Find a convex polygon with num_vertex=10 vertices where every vertex v has at least 4 other vertices approximately equidistant from v. This would be a counterexample to the conjecture that every convex polygon has at least one vertex with fewer than 4 equidistant neighbours.

Score = minimum over all vertices of a [0,1] equidistance quality measure. Score 1.0 = perfect counterexample where every vertex has exactly 4 equidistant neighbors.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `num_vertex: 10` |

## Scoring

The evaluator:
1. Checks convexity of the polygon.
2. For each vertex v, checks whether it has ≥4 equidistant neighbors.
3. Returns the minimum quality measure across all vertices.

## Known Results

- The conjecture states no such counterexample exists.
- AlphaEvolve explored near-counterexamples with quality close to 1.0.
- Score 1.0 is listed as `known_best_score` but may be an aspirational target.

## Source

[AlphaEvolve repository of problems](https://github.com/google-deepmind/alphaevolve_repository_of_problems)
