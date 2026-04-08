"""Tests for the problem evaluators via run_evaluation()."""

import numpy as np
import pytest

from autoresearch_problems import registry, run_evaluation


# ── Cap Set ──────────────────────────────────────────────────────────────────

@pytest.fixture
def cap_set_spec():
    return registry.load("combinatorics/cap_set")


def test_cap_set_valid_trivial(cap_set_spec):
    """A single vector is a valid cap set of size 1."""
    result = run_evaluation(cap_set_spec, np.array([[0, 0, 0, 0, 0, 0, 0, 0]]))
    assert result.valid
    assert result.score == 1.0


def test_cap_set_valid_two_vectors(cap_set_spec):
    """Two vectors can never form a three-term AP by themselves."""
    S = np.array([[0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0]])
    result = run_evaluation(cap_set_spec, S)
    assert result.valid
    assert result.score == 2.0


def test_cap_set_invalid_progression(cap_set_spec):
    """Three vectors forming x+y+z≡0 (mod 3) should be rejected."""
    # 0+1+2 = 3 ≡ 0 (mod 3) in every coordinate
    S = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [2, 2, 2, 2, 2, 2, 2, 2],
    ])
    result = run_evaluation(cap_set_spec, S)
    assert not result.valid
    assert result.score == 0.0


def test_cap_set_wrong_shape(cap_set_spec):
    result = run_evaluation(cap_set_spec, np.ones((5, 4), dtype=int))
    assert not result.valid


def test_cap_set_out_of_range(cap_set_spec):
    bad = np.full((2, 8), 5, dtype=int)
    result = run_evaluation(cap_set_spec, bad)
    assert not result.valid


# ── Circle Packing ────────────────────────────────────────────────────────────

@pytest.fixture
def circle_packing_spec():
    return registry.load("geometry/circle_packing")


def test_circle_packing_grid_is_valid(circle_packing_spec):
    """A simple 5×6 grid of 26 points should be valid."""
    n = 26
    cols, rows = 6, 5
    xs = np.linspace(0.0, 1.0, cols)
    ys = np.linspace(0.0, 1.0, rows)
    grid = np.array([[x, y] for y in ys for x in xs])[:n]
    result = run_evaluation(circle_packing_spec, grid)
    assert result.valid
    assert result.score > 0.0


def test_circle_packing_wrong_count(circle_packing_spec):
    result = run_evaluation(circle_packing_spec, np.random.rand(10, 2))
    assert not result.valid


def test_circle_packing_out_of_bounds(circle_packing_spec):
    pts = np.random.rand(26, 2)
    pts[0] = [-0.1, 0.5]
    result = run_evaluation(circle_packing_spec, pts)
    assert not result.valid


def test_circle_packing_all_same_point(circle_packing_spec):
    pts = np.zeros((26, 2))
    result = run_evaluation(circle_packing_spec, pts)
    assert result.valid
    assert result.score == 0.0


# ── Online Bin Packing ────────────────────────────────────────────────────────

@pytest.fixture
def bin_packing_spec():
    return registry.load("combinatorics/online_bin_packing")


def test_bin_packing_first_fit_is_valid(bin_packing_spec):
    """The first-fit heuristic should always produce a valid result."""
    def first_fit(item_size, bins):
        for i, rem in enumerate(bins):
            if rem >= item_size:
                return i
        return -1

    result = run_evaluation(bin_packing_spec, first_fit)
    assert result.valid
    assert result.score < 0  # negative number of bins
    assert result.metrics["num_bins"] > 0


def test_bin_packing_not_callable(bin_packing_spec):
    result = run_evaluation(bin_packing_spec, "not a function")
    assert not result.valid
    assert result.score == 0.0


def test_bin_packing_bad_index(bin_packing_spec):
    """Returning an out-of-range bin index should produce an invalid result."""
    def bad_heuristic(item_size, bins):
        return 9999  # always out of range

    result = run_evaluation(bin_packing_spec, bad_heuristic)
    assert not result.valid


# ── Erdős Minimum Overlap ─────────────────────────────────────────────────────

@pytest.fixture
def erdos_spec():
    return registry.load("analysis/erdos_min_overlap")


def test_erdos_valid_uniform(erdos_spec):
    """Uniform h = 0.5 over n=100 points satisfies the integral constraint."""
    n = 100
    h = np.full(n, 0.5)  # sum * (2/n) = 0.5 * 2 = 1.0
    result = run_evaluation(erdos_spec, h)
    assert result.valid
    assert result.score > 0.0


def test_erdos_invalid_out_of_range(erdos_spec):
    """Values outside [0, 1] must be rejected."""
    n = 50
    h = np.full(n, 2.0)
    result = run_evaluation(erdos_spec, h)
    assert not result.valid


def test_erdos_invalid_integral(erdos_spec):
    """Integral != 1 must be rejected."""
    n = 100
    h = np.full(n, 0.9)  # integral = 0.9 * 2 ≠ 1
    result = run_evaluation(erdos_spec, h)
    assert not result.valid


def test_erdos_invalid_empty(erdos_spec):
    result = run_evaluation(erdos_spec, [])
    assert not result.valid


def test_erdos_invalid_wrong_type(erdos_spec):
    result = run_evaluation(erdos_spec, "not an array")
    assert not result.valid


def test_erdos_multi_variants(erdos_spec):
    """initial_programs and initial_prompts dicts should be populated."""
    assert "open_evolve" in erdos_spec.initial_programs
    assert "test_time" in erdos_spec.initial_programs
    assert "open_evolve" in erdos_spec.initial_prompts


# ── Second Autocorrelation Inequality ────────────────────────────────────────

@pytest.fixture
def second_autocorr_spec():
    return registry.load("analysis/second_autocorr_ineq")


def test_second_autocorr_valid(second_autocorr_spec):
    """A uniform positive sequence should be valid."""
    seq = [1.0] * 100
    result = run_evaluation(second_autocorr_spec, seq)
    assert result.valid
    assert result.score > 0.0


def test_second_autocorr_numpy_input(second_autocorr_spec):
    seq = np.ones(50) * 2.0
    result = run_evaluation(second_autocorr_spec, seq)
    assert result.valid


def test_second_autocorr_invalid_empty(second_autocorr_spec):
    result = run_evaluation(second_autocorr_spec, [])
    assert not result.valid


def test_second_autocorr_invalid_inf(second_autocorr_spec):
    seq = [1.0, float("inf"), 1.0]
    result = run_evaluation(second_autocorr_spec, seq)
    assert not result.valid


def test_second_autocorr_invalid_wrong_type(second_autocorr_spec):
    result = run_evaluation(second_autocorr_spec, 42)
    assert not result.valid


def test_second_autocorr_multi_variants(second_autocorr_spec):
    assert "alpha_evolve" in second_autocorr_spec.initial_programs
    assert "code_evolve" in second_autocorr_spec.initial_programs
    assert "open_evolve" in second_autocorr_spec.initial_programs
    assert "theta_evolve" in second_autocorr_spec.initial_programs
    assert "alpha_evolve" in second_autocorr_spec.initial_prompts
    assert "code_evolve" in second_autocorr_spec.initial_prompts
    assert "theta_evolve" in second_autocorr_spec.initial_prompts


# ── Third Autocorrelation Inequality ─────────────────────────────────────────

@pytest.fixture
def third_autocorr_spec():
    return registry.load("analysis/third_autocorr_ineq")


def test_third_autocorr_valid(third_autocorr_spec):
    """A uniform positive sequence should be valid."""
    seq = [1.0] * 100
    result = run_evaluation(third_autocorr_spec, seq)
    assert result.valid
    assert result.score > 0.0


def test_third_autocorr_valid_with_negatives(third_autocorr_spec):
    """Sequences with negative values are allowed as long as sum != 0."""
    seq = [1.0, -0.5, 2.0, -0.3] * 25
    result = run_evaluation(third_autocorr_spec, seq)
    assert result.valid


def test_third_autocorr_invalid_zero_sum(third_autocorr_spec):
    """All-zero sequence (sum of |values| = 0) should be rejected."""
    seq = [0.0] * 10
    result = run_evaluation(third_autocorr_spec, seq)
    assert not result.valid


def test_third_autocorr_invalid_empty(third_autocorr_spec):
    result = run_evaluation(third_autocorr_spec, [])
    assert not result.valid


def test_third_autocorr_invalid_nan(third_autocorr_spec):
    seq = [1.0, float("nan"), 1.0]
    result = run_evaluation(third_autocorr_spec, seq)
    assert not result.valid


def test_third_autocorr_multi_variants(third_autocorr_spec):
    assert "alpha_evolve" in third_autocorr_spec.initial_programs
    assert "code_evolve" in third_autocorr_spec.initial_programs
    assert "open_evolve" in third_autocorr_spec.initial_programs
    assert "theta_evolve" in third_autocorr_spec.initial_programs
    assert "alpha_evolve" in third_autocorr_spec.initial_prompts
    assert "code_evolve" in third_autocorr_spec.initial_prompts
    assert "open_evolve" in third_autocorr_spec.initial_prompts
    assert "theta_evolve" in third_autocorr_spec.initial_prompts


# ── Minimizing Max/Min Distance 2D ───────────────────────────────────────────

@pytest.fixture
def min_max_dist_2d_spec():
    return registry.load("geometry/minimizing_max_min_dist_2d")


def test_min_max_dist_2d_valid(min_max_dist_2d_spec):
    """16 distinct points should be valid."""
    np.random.seed(42)
    pts = np.random.randn(16, 2)
    result = run_evaluation(min_max_dist_2d_spec, pts)
    assert result.valid
    assert result.score > 0.0


def test_min_max_dist_2d_wrong_count(min_max_dist_2d_spec):
    result = run_evaluation(min_max_dist_2d_spec, np.random.rand(10, 2))
    assert not result.valid


def test_min_max_dist_2d_wrong_dim(min_max_dist_2d_spec):
    result = run_evaluation(min_max_dist_2d_spec, np.random.rand(16, 3))
    assert not result.valid


def test_min_max_dist_2d_nan(min_max_dist_2d_spec):
    pts = np.random.randn(16, 2)
    pts[0, 0] = float("nan")
    result = run_evaluation(min_max_dist_2d_spec, pts)
    assert not result.valid


def test_min_max_dist_2d_all_same(min_max_dist_2d_spec):
    """All points at the same location → max_dist = 0, score = 0."""
    pts = np.zeros((16, 2))
    result = run_evaluation(min_max_dist_2d_spec, pts)
    assert result.valid
    assert result.score == 0.0


# ── Minimizing Max/Min Distance 3D ───────────────────────────────────────────

@pytest.fixture
def min_max_dist_3d_spec():
    return registry.load("geometry/minimizing_max_min_dist_3d")


def test_min_max_dist_3d_valid(min_max_dist_3d_spec):
    """14 distinct points should be valid."""
    np.random.seed(42)
    pts = np.random.randn(14, 3)
    result = run_evaluation(min_max_dist_3d_spec, pts)
    assert result.valid
    assert result.score > 0.0


def test_min_max_dist_3d_wrong_count(min_max_dist_3d_spec):
    result = run_evaluation(min_max_dist_3d_spec, np.random.rand(16, 3))
    assert not result.valid


def test_min_max_dist_3d_wrong_dim(min_max_dist_3d_spec):
    result = run_evaluation(min_max_dist_3d_spec, np.random.rand(14, 2))
    assert not result.valid


def test_min_max_dist_3d_nan(min_max_dist_3d_spec):
    pts = np.random.randn(14, 3)
    pts[0, 0] = float("nan")
    result = run_evaluation(min_max_dist_3d_spec, pts)
    assert not result.valid


def test_min_max_dist_3d_all_same(min_max_dist_3d_spec):
    """All points at the same location → max_dist = 0, score = 0."""
    pts = np.zeros((14, 3))
    result = run_evaluation(min_max_dist_3d_spec, pts)
    assert result.valid
    assert result.score == 0.0
