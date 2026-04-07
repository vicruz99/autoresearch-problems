import numpy as np


def solve(r1: float = 10.0, j: int = 500, **kwargs) -> np.ndarray:
    """Return values of two functions f and g on the grid.

    Grid: xs = np.linspace(-r1, (j-1)*r1/j, 2*j)

    The evaluator computes Young's convolution quotient
        Q(f, g) = ||f * g||_{L^r} / (||f||_{L^p} * ||g||_{L^q})
    with p=4/3, q=7/5, r=28/13 ≈ 2.154.

    Returns
    -------
    np.ndarray of shape (2, 2*j)
        Row 0: values of f.
        Row 1: values of g.
    """
    j = int(j)
    xs = np.linspace(-r1, (j - 1) * r1 / j, 2 * j)

    # EVOLVE-BLOCK-START
    # Box functions — simple starting point; Gaussians are near-optimal.
    f_values = (np.abs(xs) < 1.0).astype(float)
    g_values = (np.abs(xs) < 1.0).astype(float)
    # EVOLVE-BLOCK-END

    return np.stack([f_values, g_values])
