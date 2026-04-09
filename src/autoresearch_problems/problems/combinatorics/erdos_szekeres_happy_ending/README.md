# Erdős-Szekeres Happy Ending

**Category:** combinatorics  
**Optimize:** Maximize `score` (minimize convex n-gons)  
**Known best:** open

## Problem Statement

Find a configuration of exactly 2^(n−2) + 1 = 17 points in the plane in general position (no 3 collinear) that minimizes the number of convex n-gons (n=6) among them.

Score = −(number of convex 6-gons); higher (less negative) is better.

The Erdős-Szekeres theorem guarantees that any set of 2^(n−2)+1 points in general position contains at least one convex n-gon. The Happy Ending problem asks: what is the minimum number of such n-gons?

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `n: 6` |

## Scoring

The evaluator:
1. Checks that 17 points are in general position (no 3 collinear).
2. Counts the number of convex 6-gons (subsets of 6 points forming a convex hexagon).
3. Returns score = −(count of convex 6-gons).

## Known Results

- Erdős-Szekeres theorem: any 2^(n−2)+1 points in general position contain a convex n-gon.
- For n=4: exactly 5 points needed; the minimum convex 4-gons is 1.
- For n=6: the exact minimum over 17 points is open; AlphaEvolve explored this.

## Source

[AlphaEvolve repository of problems](https://github.com/google-deepmind/alphaevolve_repository_of_problems)
