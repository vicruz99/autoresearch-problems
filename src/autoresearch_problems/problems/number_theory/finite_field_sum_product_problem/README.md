# Finite Field Sum-Product Problem

**Category:** number_theory  
**Optimize:** Minimize `score`  
**Known best:** open

## Problem Statement

Construct sets X ⊆ F_p (of size ⌊√p⌋) for multiple primes p that minimize:

    log(max(|X + X|, |X · X|)) / log(|X|)

where X + X = {x + y mod p : x, y ∈ X} and X · X = {x · y mod p : x, y ∈ X}. The final score is the average over primes {101, 257, 1009}. Lower is better.

The sum-product conjecture states that max(|A+A|, |A·A|) ≥ |A|^{4/3} for any set A in a field, implying ratio ≥ 4/3 ≈ 1.33. Constructions achieving low ratio challenge this conjecture.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `primes: [101, 257, 1009]` |

## Scoring

Average of log(max(|X+X|,|X·X|))/log(|X|) over primes; lower is better. AlphaEvolve found constructions achieving average ratio ≈ 1.5 using AP∩GP.

## Known Results

- Erdős-Szemerédi conjecture: max(|A+A|, |A·A|) ≥ |A|^{2−ε}.
- Sum-product theorem over F_p: ratio ≥ 1.5 (Bourgain-Katz-Tao).
- Arithmetic progressions give |X+X| ≈ 2|X| but large |X·X|.
- AlphaEvolve used intersections of arithmetic and geometric progressions.

## Source

[AlphaEvolve repository of problems](https://github.com/google-deepmind/alphaevolve_repository_of_problems)
