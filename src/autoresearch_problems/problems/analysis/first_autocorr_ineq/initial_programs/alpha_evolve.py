import numpy as np
import time
from scipy import optimize


def solve() -> list:
    """Search for the best coefficient sequence minimizing C₁."""
    best_sequence = [np.random.random()] * np.random.randint(100, 1000)
    curr_sequence = best_sequence.copy()
    best_score = float("inf")
    start_time = time.time()
    while time.time() - start_time < 55:
        h_function = _get_good_direction(curr_sequence)
        if h_function is None:
            curr_sequence[1] = (curr_sequence[1] + np.random.rand()) % 1
        else:
            curr_sequence = h_function
        curr_score = _evaluate_sequence(curr_sequence)
        if curr_score < best_score:
            best_score = curr_score
            best_sequence = curr_sequence
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


def _evaluate_sequence(sequence):
    if not sequence:
        return float("inf")
    sequence = [float(x) for x in sequence]
    sequence = [max(0, x) for x in sequence]
    sequence = [min(1000.0, x) for x in sequence]
    n = len(sequence)
    b_sequence = np.convolve(sequence, sequence)
    max_b = max(b_sequence)
    sum_a = np.sum(sequence)
    if sum_a < 0.01:
        return float("inf")
    return float(2 * n * max_b / (sum_a ** 2))
