"""Tests for the problem registry."""

import pytest

from autoresearch_problems import registry
from autoresearch_problems.core.spec import ProblemSpec


def test_list_categories_returns_non_empty():
    categories = registry.list_categories()
    assert len(categories) > 0
    assert "combinatorics" in categories
    assert "geometry" in categories
    assert "analysis" in categories


def test_list_problems_returns_all():
    problems = registry.list_problems()
    assert "combinatorics/cap_set" in problems
    assert "combinatorics/online_bin_packing" in problems
    assert "geometry/circle_packing" in problems
    assert "geometry/kissing_number_3d" in problems
    assert "geometry/kissing_number_11d" in problems
    assert "analysis/kissing_number" not in problems


def test_list_problems_filtered_by_category():
    combinatorics = registry.list_problems(category="combinatorics")
    assert all(p.startswith("combinatorics/") for p in combinatorics)
    geometry = registry.list_problems(category="geometry")
    assert all(p.startswith("geometry/") for p in geometry)
    analysis = registry.list_problems(category="analysis")
    assert all(p.startswith("analysis/") for p in analysis)


def test_load_cap_set_returns_problem_spec():
    spec = registry.load("combinatorics/cap_set")
    assert isinstance(spec, ProblemSpec)
    assert spec.name == "cap_set"
    assert spec.category == "combinatorics"
    assert spec.evaluator_entrypoint == "evaluate"
    assert spec.evaluator_code != ""
    assert spec.maximize is True


def test_load_cap_set_has_function_name():
    """ProblemSpec.function_name should be loaded from spec.yaml."""
    spec = registry.load("combinatorics/cap_set")
    assert hasattr(spec, "function_name")
    assert spec.function_name == "solve"


def test_load_circle_packing_returns_problem_spec():
    spec = registry.load("geometry/circle_packing")
    assert isinstance(spec, ProblemSpec)
    assert spec.name == "circle_packing"
    assert spec.parameters["n"] == 26


def test_load_online_bin_packing_returns_problem_spec():
    spec = registry.load("combinatorics/online_bin_packing")
    assert isinstance(spec, ProblemSpec)
    assert spec.parameters["num_items"] == 100


def test_load_kissing_number_3d_returns_problem_spec():
    spec = registry.load("geometry/kissing_number_3d")
    assert isinstance(spec, ProblemSpec)
    assert spec.name == "kissing_number_3d"
    assert spec.category == "geometry"
    assert spec.parameters["dimension"] == 3
    assert spec.known_best_score == 12


def test_load_problem_has_optional_files():
    spec = registry.load("combinatorics/cap_set")
    assert spec.initial_prompt is not None and len(spec.initial_prompt) > 0
    assert spec.initial_program is not None and len(spec.initial_program) > 0


def test_load_kissing_number_3d_has_optional_files():
    spec = registry.load("geometry/kissing_number_3d")
    assert spec.initial_prompt is not None and len(spec.initial_prompt) > 0
    assert spec.initial_program is not None and len(spec.initial_program) > 0


def test_load_nonexistent_problem_raises():
    with pytest.raises(FileNotFoundError):
        registry.load("combinatorics/does_not_exist")


def test_problem_spec_has_no_evaluate_method():
    """ProblemSpec must NOT have an evaluate() method."""
    spec = registry.load("combinatorics/cap_set")
    assert not hasattr(spec, "evaluate")


# ── registry.load() with field overrides ─────────────────────────────────────

def test_load_with_parameters_override_merges():
    """parameters override should merge with spec.yaml values, caller wins."""
    spec = registry.load("combinatorics/cap_set", parameters={"n": 10})
    assert spec.parameters["n"] == 10
    assert spec.parameters["q"] == 3  # preserved from spec.yaml


def test_load_with_parameters_override_full_replace():
    """Passing all parameters replaces them entirely via merge."""
    spec = registry.load("combinatorics/cap_set", parameters={"n": 5, "q": 2})
    assert spec.parameters["n"] == 5
    assert spec.parameters["q"] == 2


def test_load_with_scalar_field_override():
    """Scalar fields like known_best_score are directly replaced."""
    spec = registry.load("analysis/kissing_number", known_best_score=99.0)
    assert spec.known_best_score == 99.0


def test_load_with_combined_overrides():
    """Multiple field overrides can be combined."""
    spec = registry.load(
        "analysis/kissing_number",
        parameters={"d": 4},
        known_best_score=24.0,
    )
    assert spec.parameters["d"] == 4
    assert spec.known_best_score == 24.0


def test_load_without_overrides_unchanged():
    """Calling load() with no overrides behaves exactly as before."""
    spec = registry.load("combinatorics/cap_set")
    assert spec.parameters["n"] == 8
    assert spec.parameters["q"] == 3
