# Ring Loading Problem

**Category:** combinatorics  
**Optimize:** Maximize `score`  
**Known best:** open

## Problem Statement

Find m=15 pairs (u_i, v_i) with u_i + v_i ≤ 1 to maximize alpha, defined as the minimum over all sign choices z_i ∈ {v_i, −u_i} of the maximum circular imbalance:

    max_k |Σ_{i=1}^{k} z_i − Σ_{i=k+1}^{m} z_i|

Higher alpha is better — a high alpha means all sign-choice configurations have high imbalance, which relates to the hardness of the ring loading problem.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `list` |
| Parameters | `m: 15` |

## Scoring

The evaluator:
1. Interprets the list as m pairs (u_i, v_i).
2. Checks validity: u_i, v_i ≥ 0, u_i + v_i ≤ 1.
3. Returns alpha = min over all sign choices of max circular imbalance.

## Known Results

- The ring loading problem asks for the minimum max-flow on a ring network.
- AlphaEvolve explored constructions that maximize the worst-case behavior.
- Exact optimum is unknown.

## Source

Google DeepMind / AlphaEvolve (Apache 2.0)
