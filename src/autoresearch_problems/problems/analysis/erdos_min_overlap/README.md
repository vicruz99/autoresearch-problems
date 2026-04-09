# Erdős Minimum Overlap

**Category:** analysis  
**Optimize:** Minimize `score`  
**Known best:** C₅ ≤ 0.3809

## Problem Statement

Find a step function h: [0,2] → [0,1] with ∫h = 1 that minimizes the Erdős minimum overlap constant:

    C₅ = max_k ∫h(x)(1 - h(x + k)) dx

The Erdős minimum overlap problem asks: what is the smallest possible value of C₅? Lower is better. AlphaEvolve (Google DeepMind) achieved C₅ ≤ 0.3809, improving on the previous best.

The function h is discretized into a numpy array of values on a uniform grid over [0, 2].

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | none (empty dict) |

## Scoring

The evaluator:
1. Interprets the returned array as the values of h on a uniform grid over [0, 2].
2. Clips values to [0, 1] and normalizes so ∫h = 1.
3. Computes C₅ = max_k ∫h(x)(1 − h(x + k)) dx via convolution.
4. Returns score = C₅ (lower is better).

## Known Results

- Classical lower bound: C₅ ≥ 3/8 = 0.375 (Erdős, 1955).
- AlphaEvolve achieved C₅ ≤ 0.38092303510845016.
- The exact value of the minimum C₅ is an open problem.

## Source

AlphaEvolve (Google DeepMind) — [Mathematical Discovery at Scale](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)
