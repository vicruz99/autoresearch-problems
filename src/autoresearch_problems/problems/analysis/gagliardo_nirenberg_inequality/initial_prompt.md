## Gagliardo-Nirenberg Inequality

Act as a specialist in mathematical analysis and optimisation.

Your goal is to find a Python function `solve()` that returns a 1-D NumPy
array of function values `f_values` of shape **(1001,)**, representing a
function f evaluated on the symmetric grid

```python
xs = np.linspace(-15.0, 15.0, 1001)   # R1=15.0, J=500
```

### Objective

Maximise the **Gagliardo-Nirenberg quotient**

$$Q(f) = \frac{\|f\|_p^{4p}}{\|f\|_2^{2(p+2)}\,\|f'\|_2^{2(p-2)}},
\quad p = 4.$$

The evaluator computes norms using the trapezoidal rule and approximates
`f'` via central finite differences.

### Known optimum

For p = 4 the optimal function is

$$f(x) = \operatorname{sech}(x) = \frac{1}{\cosh(x)},$$

which achieves **Q(sech) = 1/9 ≈ 0.1111**.

More generally, the optimiser for exponent p is
`f(x) = sech^{1/k}(kx)` where `k = (p-2)/2`.

### Constraints

- `f_values` must have shape `(1001,)`.
- All values must be finite.
- `|f(x)| ≤ 1e5` for all grid points.
- Both f and f' must have non-negligible L² norms (> 1e-8).

### Scoring

`score = ||f||_4^16 / (||f||_2^12 * ||f'||_2^4)` — higher is better.

```python
import numpy as np

R1 = 15.0
J  = 500

def solve() -> np.ndarray:
    xs = np.linspace(-R1, R1, 2 * J + 1)
    # EVOLVE-BLOCK-START
    f_values = np.exp(-(xs ** 2))
    # EVOLVE-BLOCK-END
    return f_values
```
