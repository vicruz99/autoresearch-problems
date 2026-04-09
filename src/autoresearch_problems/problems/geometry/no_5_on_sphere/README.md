# No 5 on a Sphere

**Category:** geometry  
**Optimize:** Maximize `score`  
**Known best:** open

## Problem Statement

Place as many points as possible on the unit sphere (in R³) such that no 5 points lie on any common great circle (i.e., no 5 points are coplanar with the origin). Score = number of valid points placed (out of up to n=50 attempted).

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `n: 50` |

## Scoring

The evaluator:
1. Normalizes all points to the unit sphere.
2. Checks every quintuple of points: no 5 should be coplanar with the origin.
3. Returns the count of valid points (those not part of any violating 5-coplanar group — or the max valid subset).

## Known Results

- Any 4 points on a sphere lie on a great circle (great circle is defined by any 2 non-antipodal points); the constraint is stronger: no 5.
- The maximum is an open combinatorial geometry problem.
- AlphaEvolve explored this as a combinatorial extremal problem on the sphere.

## Source

Google DeepMind / AlphaEvolve (Apache 2.0)
