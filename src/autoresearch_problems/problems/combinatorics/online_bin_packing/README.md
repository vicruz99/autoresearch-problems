# Online Bin Packing

**Category:** combinatorics  
**Optimize:** Maximize `score` (fewer bins)  
**Known best:** open

## Problem Statement

Design an online bin-packing heuristic: items with sizes in (0, 1] arrive one at a time and must be assigned immediately and irrevocably to a bin of capacity 1.0. The goal is to minimize the total number of bins used over 100 items (seed=42).

Score = −(number of bins used); higher = fewer bins = better.

This is the classic online bin packing problem. Your `solve` function must return a **function** (the heuristic), not a value.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `callable` |
| Parameters | `num_items: 100`, `seed: 42` |

## Scoring

The evaluator:
1. Calls `solve()` to get the heuristic function `h`.
2. Generates 100 random item sizes from seed 42.
3. For each item, calls `h(item_size, bins)` to get a bin index.
4. Returns score = −(total bins used).

## Known Results

- First Fit Decreasing (offline) achieves OPT + 6/9·OPT bins.
- Best Fit (online) achieves at most 1.7·OPT bins.
- FunSearch (DeepMind) found improved online heuristics using program evolution.

## Source

FunSearch (DeepMind)
