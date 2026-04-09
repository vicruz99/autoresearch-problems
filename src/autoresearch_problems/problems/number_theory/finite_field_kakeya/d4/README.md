# Finite Field Kakeya (d=4)

**Category:** number_theory  
**Optimize:** Maximize `score`  
**Known best:** open (AlphaEvolve found elliptic-curve-linked constructions)

## Problem Statement

Find minimum-size Kakeya sets in F_p^4 for primes p ∈ {3, 5, 7}. A Kakeya set must contain a line in every direction.

Score = average −(|K(p)| / reference_size(p, 4)) over primes {3, 5, 7}.

AlphaEvolve found constructions for d=4 with links to elliptic curves (manually verified by mathematicians).

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `d: 4`, `primes: [3, 5, 7]` |

## Scoring

Average −|K(p)|/reference over primes {3,5,7}.

## Known Results

- d=4 is computationally harder than d=3 (p^4 points per prime).
- AlphaEvolve found constructions linked to elliptic curves over F_p — a surprising algebraic structure.
- Timeout is extended to 300 seconds for this problem.
- For p=7: 7^4 = 2401 points total.

## Source

[AlphaEvolve repository of problems](https://github.com/google-deepmind/alphaevolve_repository_of_problems)
