"""Tests for the problem evaluators via ProblemSpec.evaluate()."""

import numpy as np
import pytest

from autoresearch_problems import registry


# ── Cap Set ──────────────────────────────────────────────────────────────────

@pytest.fixture
def cap_set_spec():
    return registry.load("combinatorics/cap_set")


def test_cap_set_valid_trivial(cap_set_spec):
    """A single vector is a valid cap set of size 1."""
    result = cap_set_spec.evaluate(np.array([[0, 0, 0, 0, 0, 0, 0, 0]]))
    assert result.valid
    assert result.score == 1.0


def test_cap_set_valid_two_vectors(cap_set_spec):
    """Two vectors can never form a three-term AP by themselves."""
    S = np.array([[0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0]])
    result = cap_set_spec.evaluate(S)
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
    result = cap_set_spec.evaluate(S)
    assert not result.valid
    assert result.score == 0.0


def test_cap_set_wrong_shape(cap_set_spec):
    result = cap_set_spec.evaluate(np.ones((5, 4), dtype=int))
    assert not result.valid


def test_cap_set_out_of_range(cap_set_spec):
    bad = np.full((2, 8), 5, dtype=int)
    result = cap_set_spec.evaluate(bad)
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
    result = circle_packing_spec.evaluate(grid)
    assert result.valid
    assert result.score > 0.0


def test_circle_packing_wrong_count(circle_packing_spec):
    result = circle_packing_spec.evaluate(np.random.rand(10, 2))
    assert not result.valid


def test_circle_packing_out_of_bounds(circle_packing_spec):
    pts = np.random.rand(26, 2)
    pts[0] = [-0.1, 0.5]
    result = circle_packing_spec.evaluate(pts)
    assert not result.valid


def test_circle_packing_all_same_point(circle_packing_spec):
    pts = np.zeros((26, 2))
    result = circle_packing_spec.evaluate(pts)
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

    result = bin_packing_spec.evaluate(first_fit)
    assert result.valid
    assert result.score < 0  # negative number of bins
    assert result.metrics["num_bins"] > 0


def test_bin_packing_not_callable(bin_packing_spec):
    result = bin_packing_spec.evaluate("not a function")
    assert not result.valid
    assert result.score == 0.0


def test_bin_packing_bad_index(bin_packing_spec):
    """Returning an out-of-range bin index should produce an invalid result."""
    def bad_heuristic(item_size, bins):
        return 9999  # always out of range

    result = bin_packing_spec.evaluate(bad_heuristic)
    assert not result.valid
