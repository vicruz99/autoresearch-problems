# Finite Field Kakeya (d=3)

**Category:** number_theory  
**Optimize:** Maximize `score`  
**Known best:** open (AlphaEvolve improved lower bound with Lean-verified proof)

## Problem Statement

Find minimum-size Kakeya sets in F_p^3 for primes p ∈ {3, 5, 7, 11}. A Kakeya set must contain a line in every direction.

Score = average −(|K(p)| / reference_size(p, 3)) over tested primes.

This is the most celebrated sub-problem: **AlphaEvolve found a new construction for d=3 that was verified with a complete Lean 4 formal proof** — the first machine-discovered improvement to a classical combinatorics bound with a fully machine-verified proof.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `d: 3`, `primes: [3, 5, 7, 11]` |

## Scoring

Average −|K(p)|/reference over primes {3,5,7,11}.

## Known Results

- AlphaEvolve discovered a new construction in d=3 with a Lean 4 proof.
- This was a landmark result: first AI-discovered, formally-proved improvement in finite combinatorics.
- The construction improved on the Saraf-Sudan bound for d=3.
- Primes tested: [3, 5, 7, 11].

## Source

[AlphaEvolve repository of problems](https://github.com/google-deepmind/alphaevolve_repository_of_problems) — see the "Mathematical Discovery at Scale" paper for the Lean proof.
