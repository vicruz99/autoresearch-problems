import numpy as np

# Fixed grid parameters (must match evaluator)
R1 = 10.0
J = 500


def solve() -> np.ndarray:
    """Return values of two functions f and g on the grid.

    Grid: xs = np.linspace(-R1, (J-1)*R1/J, 2*J)

    The evaluator computes Young's convolution quotient
        Q(f, g) = ||f * g||_{L^r} / (||f||_{L^p} * ||g||_{L^q})
    with p=4/3, q=7/5, r=28/13 ≈ 2.154.

    Returns
    -------
    np.ndarray of shape (2, 2*J) = (2, 1000)
        Row 0: values of f.
        Row 1: values of g.
    """
    xs = np.linspace(-R1, (J - 1) * R1 / J, 2 * J)

    # EVOLVE-BLOCK-START
    # Box functions — simple starting point; Gaussians are near-optimal.
    f_values = (np.abs(xs) < 1.0).astype(float)
    g_values = (np.abs(xs) < 1.0).astype(float)
    # EVOLVE-BLOCK-END

    return np.stack([f_values, g_values])
