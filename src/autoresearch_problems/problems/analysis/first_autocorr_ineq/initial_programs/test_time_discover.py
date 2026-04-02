import numpy as np
from scipy import optimize


def solve() -> list:
    """Search for the best coefficient sequence minimizing C₁ (single step)."""
    best_sequence = [np.random.random()] * np.random.randint(100, 1000)
    h_function = _get_good_direction(best_sequence)
    if h_function is None:
        best_sequence[1] = (best_sequence[1] + np.random.rand()) % 1
    else:
        best_sequence = h_function
    return best_sequence


def _solve_convolution_lp(f_sequence, rhs):
    n = len(f_sequence)
    c = -np.ones(n)
    a_ub = []
    b_ub = []
    for k in range(2 * n - 1):
        row = np.zeros(n)
        for i in range(n):
            j = k - i
            if 0 <= j < n:
                row[j] = f_sequence[i]
        a_ub.append(row)
        b_ub.append(rhs)
    a_ub_nonneg = -np.eye(n)
    b_ub_nonneg = np.zeros(n)
    a_ub = np.vstack([a_ub, a_ub_nonneg])
    b_ub = np.hstack([b_ub, b_ub_nonneg])
    result = optimize.linprog(c, A_ub=a_ub, b_ub=b_ub)
    if result.success:
        return result.x
    return None


def _get_good_direction(sequence):
    n = len(sequence)
    sum_sequence = np.sum(sequence)
    if sum_sequence < 1e-9:
        return None
    normalized = [x * np.sqrt(2 * n) / sum_sequence for x in sequence]
    rhs = np.max(np.convolve(normalized, normalized))
    g_fun = _solve_convolution_lp(normalized, rhs)
    if g_fun is None:
        return None
    sum_g = np.sum(g_fun)
    if sum_g < 1e-9:
        return None
    normalized_g = [x * np.sqrt(2 * n) / sum_g for x in g_fun]
    t = 0.01
    return [(1 - t) * x + t * y for x, y in zip(sequence, normalized_g)]
