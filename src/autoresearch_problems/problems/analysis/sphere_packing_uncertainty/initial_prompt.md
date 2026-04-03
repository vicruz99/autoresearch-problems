# Sphere Packing Uncertainty Principle

## Problem Description

This problem is related to the **uncertainty principle** for sphere packing in dimension `n_dim=25`. The goal is to find `m=10` positive real roots `z₁ < z₂ < ... < z_m` such that a certain **linear combination of generalized Laguerre polynomials** `g(x)` — constrained to have **double zeros** at each `zᵢ` — has the **largest possible final sign change**.

## Mathematical Setting

For dimension `n` (here `n_dim=25`) with `α = n/2 - 1`, we consider functions:

```
g(x) = ∑ₖ cₖ · L_{2k+1}^α(x)
```

subject to: `g(0) = 0`, `g'(0) = 1`, and `g(zᵢ) = g'(zᵢ) = 0` for all `i = 1..m`.

The coefficients `cₖ` are determined by least squares from these constraints.

## Function Signature

```python
def solve() -> np.ndarray:
    """
    Returns:
        np.ndarray: 1D array of length m=10, positive reals in (0, 300].
                    These are the prescribed double-zero locations z_1,...,z_m.
    """
```

## Evaluation

1. Roots are sorted and the Laguerre combination coefficients are computed via least squares
2. `g(x)` is evaluated on a fine grid up to `2 * max(zᵢ)`
3. Sign changes of `g` are located
4. `score = position of the last sign change` (larger = better)

## Tips

- Start with evenly spaced roots in `[38, 180]`.
- Push roots farther apart to increase the last sign change.
- The Laguerre zeros for degree `2k+1` in dimension 25 may provide natural initial guesses.
- The relationship between roots of auxiliary functions and sphere packing densities is deep (related to Viazovska's proof for dim 8 and 24).
