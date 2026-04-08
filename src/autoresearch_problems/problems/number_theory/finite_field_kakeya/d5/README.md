# Finite Field Kakeya (d=5)

**Category:** number_theory  
**Optimize:** Maximize `score`  
**Known best:** open

## Problem Statement

Find minimum-size Kakeya sets in F_p^5 for primes p ∈ {3, 5}. A Kakeya set must contain a line in every direction.

Score = average −(|K(p)| / reference_size(p, 5)) over primes {3, 5}.

d=5 is the computationally most demanding variant; even p=5 produces 5^5=3125 points.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `d: 5`, `primes: [3, 5]` |

## Scoring

Average −|K(p)|/reference over primes {3,5}. Timeout is 600 seconds.

## Known Results

- d=5 is at the frontier of computational tractability.
- No improved constructions are known for d=5 beyond the Saraf-Sudan bound.
- Algebraic constructions from lower dimensions may generalize.

## Source

[AlphaEvolve repository of problems](https://github.com/google-deepmind/alphaevolve_repository_of_problems)
