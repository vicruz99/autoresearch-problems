# Tammes Problem (n=14)

**Category:** geometry  
**Optimize:** Maximize `score`  
**Known best:** open

## Problem Statement

Place n=14 points on the unit sphere in R³ to maximize the minimum pairwise Euclidean distance between any two points (Tammes problem).

Score = minimum pairwise distance. Higher is better.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `n: 14` |

## Scoring

The evaluator normalizes points to the unit sphere and returns the minimum pairwise Euclidean distance.

## Known Results

- Tammes problem: distribute n points on a sphere so the minimum angular separation is maximized.
- For n=14: best known configuration gives min distance ≈ 0.816 (angle ≈ 54.9°).
- The global optimum for n=14 is not rigorously verified.

## Source

Google DeepMind / AlphaEvolve (Apache 2.0)
