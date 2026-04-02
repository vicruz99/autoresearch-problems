## Hausdorff-Young Inequality

Act as a specialist in mathematical analysis and optimisation.

Your goal is to find a Python function `solve()` that returns a 1-D NumPy
array of function values `f_values` of shape **(1000,)**, representing a
function f evaluated on the grid

```python
xs = np.linspace(-5.0, 4.99, 1000)   # R1=5.0, J=500
```

### Objective

Maximise the **Hausdorff-Young quotient**

$$Q(f) = \frac{\|\hat{f}\|_{L^q(\mathbb{R})}}{\|f\|_{L^p(\mathbb{R})}},
\quad p = \tfrac{3}{2},\quad q = 3.$$

The evaluator treats `f_values` as a piecewise-constant function, computes
the L^p norm analytically, then computes the Fourier transform of the
piecewise-constant approximation and its L^q norm via Gauss-Legendre
quadrature over `[-10, 10]`.

### Known bound

The sharp **Babenko-Beckner constant** for p = 3/2 is

$$A_p = \left(\frac{p^{1/p}}{q^{1/q}}\right)^{1/2} \approx 0.9532.$$

The optimal function achieving this bound is a **Gaussian** `f(x) = exp(-αx²)`
for any α > 0.

### Constraints

- `f_values` must have shape `(1000,)`.
- All values must be finite.
- `|f(x)| ≤ 100` for all grid points.
- The function must be non-zero (L^p norm > 1e-15).

### Scoring

`score = ||f_hat||_{L^3} / ||f||_{L^{3/2}}` — higher is better.

```python
import numpy as np

R1 = 5.0
J  = 500

def solve() -> np.ndarray:
    xs = np.linspace(-R1, (J - 1) * R1 / J, 2 * J)
    # EVOLVE-BLOCK-START
    f_values = np.exp(-np.abs(xs))
    # EVOLVE-BLOCK-END
    return f_values
```
