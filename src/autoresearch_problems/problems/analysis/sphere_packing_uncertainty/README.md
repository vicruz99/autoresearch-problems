# Sphere Packing Uncertainty Principle

**Category:** analysis  
**Optimize:** Maximize `score`  
**Known best:** open

## Problem Statement

Find m = 10 positive real roots z₁, ..., z_m for a linear combination of generalized Laguerre polynomials g(x) in dimension n_dim = 25, such that g has double zeros at each z_i. Maximize the largest sign change of g.

This problem is related to the linear programming bounds for sphere packing (Cohn-Elkies), where auxiliary functions with prescribed zero structure provide upper bounds on sphere packing density.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `numpy_array` |
| Parameters | `m: 10`, `n_dim: 25` |

## Scoring

The evaluator:
1. Interprets the array as m positive real root positions.
2. Constructs the Laguerre polynomial combination with double zeros at those positions.
3. Returns the largest sign change measure (higher is better).

## Known Results

- Connected to Viazovska's proof of sphere packing optimality in dimensions 8 and 24.
- AlphaEvolve used this as a benchmark for exploring the uncertainty principle constraints.
- Exact optimum is unknown.

## Source

Google DeepMind / AlphaEvolve (Apache 2.0)
