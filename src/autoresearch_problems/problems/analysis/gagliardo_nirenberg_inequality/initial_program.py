import numpy as np


def solve(r1: float = 15.0, j: int = 500, **kwargs) -> np.ndarray:
    """Return function values on grid xs = np.linspace(-r1, r1, 2*j+1).

    The evaluator computes the Gagliardo-Nirenberg quotient
        Q(f) = ||f||_p^{4p} / (||f||_2^{2(p+2)} * ||f'||_2^{2(p-2)})  (p=4)
    from these values.  The known optimal is f(x) = 1/cosh(x) = sech(x).

    Returns
    -------
    np.ndarray of shape (2*j+1,)
    """
    j = int(j)
    xs = np.linspace(-r1, r1, 2 * j + 1)

    # EVOLVE-BLOCK-START
    # Gaussian — a reasonable starting point, but sech(x) achieves Q = 1/9.
    f_values = np.exp(-(xs ** 2))
    # EVOLVE-BLOCK-END

    return f_values
