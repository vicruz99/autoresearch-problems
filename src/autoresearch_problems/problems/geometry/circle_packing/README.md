# Circle Packing

**Category:** geometry  
**Optimize:** Maximize `score`  
**Known best:** open

## Problem Statement

Pack n=26 non-overlapping unit-radius circles inside a unit square [0,1]² (equivalently, place n=26 points in [0,1]² to maximize the minimum pairwise Euclidean distance between them).

Score = minimum pairwise distance between any two centers. Higher is better.

This is equivalent to packing 26 equal circles in a square, a classical optimization problem studied since the 1960s.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `n: 26` |

## Scoring

The evaluator:
1. Checks that all n points are in [0,1]².
2. Computes all pairwise distances.
3. Returns score = minimum pairwise distance.

## Known Results

- Best known packing for 26 circles in a unit square: dmin ≈ 0.1786 (Packomania).
- ShinkaEvolve (Sakana AI) used this as a benchmark problem.
- Exact optimum is unknown for n=26.

## Source

ShinkaEvolve (Sakana AI) / classic packing
