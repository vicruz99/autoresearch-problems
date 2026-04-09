# Finite Field Kakeya (Parent)

**Category:** number_theory  
**Optimize:** Maximize `score`  
**Known best:** open

## Problem Statement

Find minimum-size Kakeya sets in F_p^d for multiple primes p. A Kakeya set K must contain a complete line in every direction: for every non-zero v ∈ F_p^d there exists x ∈ K such that

    { x + t·v mod p : t ∈ F_p } ⊆ K.

Following the AlphaEvolve paper ("Mathematical Discovery at Scale"), the construction is evaluated on several primes and the final score is the average normalized size −(|K(p)| / reference_size(p, d)) over all tested primes. Higher (less negative) is better.

`solve(d, primes)` returns a dict {p: array} where each array has shape (k, d) with entries in {0,...,p-1}.

Default parameters: d=3, primes=[3,5,7,11].

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `d: 3`, `primes: [3, 5, 7, 11]` |

## Scoring

The average normalized size −(|K(p)| / reference_size(p,d)) over all primes. Closer to 0 is better.

## Known Results

- The finite field Kakeya problem: what is the minimum size of a Kakeya set in F_p^d?
- Saraf-Sudan lower bound: |K| ≥ (1/2) p^d.
- AlphaEvolve found new constructions beating the Wolff lower bound for d=3.
- For d=3, AlphaEvolve's construction was verified with a complete Lean 4 proof.

## Sub-problems

See `d2/`, `d3/`, `d4/`, `d5/` for dimension-specific variants.

## Source

[AlphaEvolve repository of problems](https://github.com/google-deepmind/alphaevolve_repository_of_problems)
