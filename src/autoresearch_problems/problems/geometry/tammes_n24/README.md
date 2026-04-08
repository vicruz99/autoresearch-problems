# Tammes Problem (n=24)

**Category:** geometry  
**Optimize:** Maximize `score`  
**Known best:** open

## Problem Statement

Place n=24 points on the unit sphere in R³ to maximize the minimum pairwise Euclidean distance between any two points (Tammes problem).

Score = minimum pairwise distance. Higher is better.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `n: 24` |

## Scoring

Returns minimum pairwise distance after normalizing to unit sphere.

## Known Results

- Best known configuration for n=24: min distance ≈ 0.5765 (angle ≈ 35.2°).
- Snub cube (24 vertices, equal-edge polyhedron) is a natural candidate.
- Exact optimum for n=24 is open.

## Source

Google DeepMind / AlphaEvolve (Apache 2.0)
