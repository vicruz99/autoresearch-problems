## Young's Convolution Inequality

Act as a specialist in mathematical analysis and optimisation.

Your goal is to find a Python function `solve()` that returns a 2-D NumPy
array of shape **(2, 1000)** representing two functions f (row 0) and g
(row 1) evaluated on the grid

```python
xs = np.linspace(-R1, (J - 1) * R1 / J, 2 * J)
# with R1=10.0, J=500 this equals np.linspace(-10.0, 9.98, 1000)
```

### Objective

Maximise **Young's convolution quotient**

$$Q(f, g) = \frac{\|f * g\|_{L^r}}{\|f\|_{L^p}\,\|g\|_{L^q}},$$

with exponents

$$p = \tfrac{4}{3},\quad q = \tfrac{7}{5},\quad \frac{1}{r} = \frac{1}{p} + \frac{1}{q} - 1 \implies r = \tfrac{28}{13} \approx 2.154.$$

The evaluator uses piecewise-constant L^p/L^q norms and a discrete
convolution (`np.convolve(f, g, mode='same') * dx`) for the L^r norm.

### Known result

The sharp Young constant is achieved by **Gaussians**:
`f(x) = exp(-αx²)`, `g(x) = exp(-βx²)` for optimal α, β > 0.

### Constraints

- Output must have shape `(2, 1000)`.
- All values must be finite and `|f|, |g| ≤ 1000`.
- Both f and g must be non-zero.

### Scoring

`score = ||f*g||_{L^r} / (||f||_{L^p} * ||g||_{L^q})` — higher is better.

```python
import numpy as np

R1 = 10.0
J  = 500

def solve() -> np.ndarray:
    xs = np.linspace(-R1, (J - 1) * R1 / J, 2 * J)
    # EVOLVE-BLOCK-START
    f_values = (np.abs(xs) < 1.0).astype(float)
    g_values = (np.abs(xs) < 1.0).astype(float)
    # EVOLVE-BLOCK-END
    return np.stack([f_values, g_values])
```
