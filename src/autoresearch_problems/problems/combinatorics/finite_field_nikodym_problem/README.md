# Finite Field Nikodym Problem

**Category:** combinatorics  
**Optimize:** Maximize `score`  
**Known best:** open

## Problem Statement

Find minimum-size Nikodym sets in F_q^2 (where q = p²) for multiple primes p. A set N ⊆ F_q^2 is a Nikodym set if for every point x ∈ F_q^2 there exists a direction v ∈ F_q^2 \ {0} such that the punctured line

    { x + t·v : t ∈ F_q, t ≠ 0 }

is entirely contained in N. The score is the average normalized complement fraction (|F_q^2| − |N|) / |F_q^2| across primes p ∈ {3, 5}. Higher complement fraction = smaller Nikodym set = better score.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `d: 2`, `primes: [3, 5]` |

## Scoring

The evaluator verifies that the returned dict {p: array} contains valid Nikodym sets for each prime and returns the average normalized complement fraction.

## Known Results

- Nikodym sets must cover at least a constant fraction of F_q^2.
- AlphaEvolve found ~3.4% complement fraction for p=29.
- Exact minimum size is an open problem.

## Source

[AlphaEvolve repository of problems](https://github.com/google-deepmind/alphaevolve_repository_of_problems)
