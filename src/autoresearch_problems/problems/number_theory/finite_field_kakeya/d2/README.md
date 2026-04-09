# Finite Field Kakeya (d=2)

**Category:** number_theory  
**Optimize:** Maximize `score`  
**Known best:** open

## Problem Statement

Find minimum-size Kakeya sets in F_p^2 for primes p ∈ {3, 5, 7, 11, 13}. A Kakeya set in F_p^2 must contain a line in every direction: for every direction v ≠ 0 in F_p^2, there exists a translate that lies entirely in the set.

Score = average −(|K(p)| / reference_size(p, 2)) over tested primes. Closer to 0 is better.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `d: 2`, `primes: [3, 5, 7, 11, 13]` |

## Scoring

Average normalized size over primes; higher (closer to 0) means smaller Kakeya sets.

## Known Results

- In F_p^2, exact minimum Kakeya set sizes are computable for small p by exhaustive search.
- For p=3: minimum |K| = 6 out of 9 points.
- AlphaEvolve explored algebraic constructions that improve on random constructions.
- The d=2 case is easier than d=3+ due to smaller search space.

## Source

[AlphaEvolve repository of problems](https://github.com/google-deepmind/alphaevolve_repository_of_problems)
