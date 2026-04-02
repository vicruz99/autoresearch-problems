import numpy as np

# Fixed grid parameters (must match evaluator)
R1 = 15.0
J = 500


def solve() -> np.ndarray:
    """Return function values on grid xs = np.linspace(-R1, R1, 2*J+1).

    The evaluator computes the Gagliardo-Nirenberg quotient
        Q(f) = ||f||_p^{4p} / (||f||_2^{2(p+2)} * ||f'||_2^{2(p-2)})  (p=4)
    from these values.  The known optimal is f(x) = 1/cosh(x) = sech(x).

    Returns
    -------
    np.ndarray of shape (2*J+1,) = (1001,)
    """
    xs = np.linspace(-R1, R1, 2 * J + 1)

    # EVOLVE-BLOCK-START
    # Gaussian — a reasonable starting point, but sech(x) achieves Q = 1/9.
    f_values = np.exp(-(xs ** 2))
    # EVOLVE-BLOCK-END

    return f_values
