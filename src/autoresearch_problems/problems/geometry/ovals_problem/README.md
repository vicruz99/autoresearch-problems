# Ovals Problem

**Category:** geometry  
**Optimize:** Maximize `score` (minimize Rayleigh quotient)  
**Known best:** open

## Problem Statement

Find a convex closed planar curve (parametrized by arc-length angle, discretized into n=100 points) and a function φ on it to minimize the Rayleigh quotient:

    R = ∫(φ'² + κ² φ²) / ∫φ²

where κ is the curvature. Score = −R (maximize to minimize R).

This is related to the spectral theory of convex curves and the eigenvalue problem for the operator −d²/ds² + κ² on the curve.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `list` |
| Parameters | `n: 100` |

## Scoring

The evaluator:
1. Interprets the list as the curve + function parameterization.
2. Computes the curvature κ numerically.
3. Returns score = −R (higher = smaller Rayleigh quotient).

## Known Results

- For a circle, the minimum Rayleigh quotient is known analytically: R = 1 + (2π/L)² where L is the circumference.
- Ellipses provide a family of test curves.
- The exact minimum over all convex curves is an open problem.

## Source

Google DeepMind / AlphaEvolve (Apache 2.0)
