# Cap Set

**Category:** combinatorics  
**Optimize:** Maximize `score`  
**Known best:** open (FunSearch improved known records)

## Problem Statement

Find the largest subset S of F_3^n (the n-dimensional vector space over GF(3), with n=8) that contains no three-term arithmetic progression (3-AP). Formally, a valid cap set S satisfies: for all x, y, z ∈ S, x + y + z ≠ 0 (mod 3).

The score is |S| — the number of elements in the cap set. Larger is better.

This is one of the fundamental open problems in additive combinatorics. FunSearch (DeepMind) discovered new large cap sets in F_3^8, demonstrating AI-driven mathematical discovery.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `n: 8`, `q: 3` |

## Scoring

The evaluator:
1. Checks that every element is a valid vector in F_3^n.
2. Verifies no three elements form an arithmetic progression.
3. Returns score = |S| if valid, else 0 or penalty.

## Known Results

- Best known cap set in F_3^8 has 496 elements (found computationally).
- FunSearch improved on previous programmatic constructions.
- Upper bound: |S| ≤ 2.756^n (Croot-Lev-Pach, Ellenberg-Gijswijt, 2016).

## Source

FunSearch (DeepMind) — [Mathematical discoveries from program search with large language models](https://deepmind.google/discover/blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/)
