# Packing Unit Cubes

**Category:** geometry  
**Optimize:** Maximize `score` (minimize bounding box)  
**Known best:** open

## Problem Statement

Pack n=11 unit cubes in the smallest possible bounding cube. Cubes may be rotated arbitrarily. Score = −bounding_box_side_length (maximize = minimize bounding box).

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `n: 11` |

## Scoring

The evaluator:
1. Takes the (11, 6) array as 11 tuples `[cx, cy, cz, α, β, γ]` (center + Euler angles).
2. Computes the axis-aligned bounding box of the union of all rotated unit cubes.
3. Returns score = −side_length.

## Known Results

- 11 unit cubes can be packed in a cube of side ≈ 2.84 (better than 3 = three unit cubes in a row).
- Tilted arrangements (not axis-aligned) can reduce bounding box slightly.
- Exact minimum for n=11 is an open problem.

## Source

Google DeepMind / AlphaEvolve (Apache 2.0)
