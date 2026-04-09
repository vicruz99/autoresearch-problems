# Minimizing Max-Min Distance (2D)

**Category:** geometry  
**Optimize:** Maximize `score`  
**Known best:** 1.0

## Problem Statement

Place exactly n=16 points in 2D space to maximize the ratio of minimum to maximum pairwise distance: dmin/dmax.

Score = (dmin/dmax)² / BENCHMARK, where BENCHMARK = 1/12.889266112 (found by AlphaEvolve). A score > 1.0 means a new record.

This is related to the problem of finding the most "uniformly distributed" set of n points in the plane.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `n: 16`, `d: 2` |

## Scoring

The evaluator computes dmin/dmax over all pairs, then divides (dmin/dmax)² by the benchmark. Score ≥ 1.0 matches or beats the best known.

## Known Results

- ShinkaEvolve (Sakana AI) established the benchmark at (dmin/dmax)² ≈ 1/12.889.
- Score 1.0 means matching the benchmark.
- Problem is related to Tammes problem on sphere but in 2D plane (no boundary).

## Source

[ShinkaEvolve (Sakana AI)](https://github.com/SakanaAI/ShinkaEvolve)
