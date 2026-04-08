# Minimizing Max-Min Distance (3D)

**Category:** geometry  
**Optimize:** Maximize `score`  
**Known best:** 1.0

## Problem Statement

Place exactly n=14 points in 3D space to maximize the ratio of minimum to maximum pairwise distance: dmin/dmax.

Score = (dmin/dmax)² / BENCHMARK, where BENCHMARK = 1/4.165849767 (found by AlphaEvolve). A score > 1.0 is a new record.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `n: 14`, `d: 3` |

## Scoring

Score = (dmin/dmax)² / BENCHMARK. Score ≥ 1.0 matches or beats the best known.

## Known Results

- ShinkaEvolve established benchmark at (dmin/dmax)² ≈ 1/4.165.
- 14 points in 3D: related to the Tammes problem but without spherical constraint.

## Source

[ShinkaEvolve (Sakana AI)](https://github.com/SakanaAI/ShinkaEvolve)
