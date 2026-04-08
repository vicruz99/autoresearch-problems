# Sums and Differences

**Category:** combinatorics  
**Optimize:** Maximize `score`  
**Known best:** open

## Problem Statement

Find a set A of distinct integers to maximize the ratio:

    log|A − A| / log|A + A|

where A + A = {a + b : a, b ∈ A} and A − A = {a − b : a, b ∈ A}. Ruzsa's inequality gives |A − A| ≤ |A + A|³, which implies the ratio is at most 3. Higher ratio means the difference set is much larger than the sumset, challenging the additive combinatorics intuition.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `list` |
| Parameters | none |

## Scoring

The evaluator:
1. Checks that all elements are distinct integers.
2. Computes |A + A| and |A − A|.
3. Returns log|A − A| / log|A + A| (higher is better).

## Known Results

- Ruzsa's inequality: |A − A| ≤ |A + A|³ (ratio ≤ 3).
- For arithmetic progressions: |A + A| ≈ 2|A|, |A − A| ≈ 2|A|, ratio ≈ 1.
- Geometric progressions: |A + A| ≈ |A|² / 2, ratio can be < 1.
- AlphaEvolve sought constructions with ratio > 2, which would be remarkable.

## Source

Google DeepMind / AlphaEvolve (Apache 2.0)
