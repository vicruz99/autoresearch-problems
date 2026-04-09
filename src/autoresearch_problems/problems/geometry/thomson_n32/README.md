# Thomson Problem (n=32)

**Category:** geometry  
**Optimize:** Maximize `score` (minimize energy)  
**Known best:** open

## Problem Statement

Place n=32 point charges on the unit sphere in R³ to minimize the Thomson energy (total Coulomb repulsion):

    E = Σ_{i<j} 1 / |xᵢ − xⱼ|

Score = −E (higher = lower energy = better configuration).

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `n: 32` |

## Scoring

The evaluator computes E = Σ 1/rᵢⱼ and returns score = −E.

## Known Results

- The Thomson problem is related to optimal sphere packing and minimal energy configurations.
- For n=32, the minimum energy is approximately −E ≈ −something (see Packomania/Thomson databases).
- Best known configurations have been tabulated by Sloane et al.

## Source

Google DeepMind / AlphaEvolve (Apache 2.0)
