"""Tests for the problem registry."""

import pytest

from autoresearch_problems import registry
from autoresearch_problems.core.spec import ProblemSpec


def test_list_categories_returns_non_empty():
    categories = registry.list_categories()
    assert len(categories) > 0
    assert "combinatorics" in categories
    assert "geometry" in categories


def test_list_problems_returns_all():
    problems = registry.list_problems()
    assert "combinatorics/cap_set" in problems
    assert "combinatorics/online_bin_packing" in problems
    assert "geometry/circle_packing" in problems


def test_list_problems_filtered_by_category():
    combinatorics = registry.list_problems(category="combinatorics")
    assert all(p.startswith("combinatorics/") for p in combinatorics)
    geometry = registry.list_problems(category="geometry")
    assert all(p.startswith("geometry/") for p in geometry)


def test_load_cap_set_returns_problem_spec():
    spec = registry.load("combinatorics/cap_set")
    assert isinstance(spec, ProblemSpec)
    assert spec.name == "cap_set"
    assert spec.category == "combinatorics"
    assert spec.evaluator_entrypoint == "evaluate"
    assert spec.evaluator_code != ""
    assert spec.maximize is True


def test_load_circle_packing_returns_problem_spec():
    spec = registry.load("geometry/circle_packing")
    assert isinstance(spec, ProblemSpec)
    assert spec.name == "circle_packing"
    assert spec.parameters["n"] == 26


def test_load_online_bin_packing_returns_problem_spec():
    spec = registry.load("combinatorics/online_bin_packing")
    assert isinstance(spec, ProblemSpec)
    assert spec.parameters["num_items"] == 100


def test_load_problem_has_optional_files():
    spec = registry.load("combinatorics/cap_set")
    assert spec.initial_prompt is not None and len(spec.initial_prompt) > 0
    assert spec.initial_program is not None and len(spec.initial_program) > 0


def test_load_nonexistent_problem_raises():
    with pytest.raises(FileNotFoundError):
        registry.load("combinatorics/does_not_exist")
