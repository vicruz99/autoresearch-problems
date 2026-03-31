"""Tests for core/evaluation.py — run_evaluation()."""

import numpy as np
import pytest

from autoresearch_problems import registry, run_evaluation
from autoresearch_problems.core.evaluation import run_evaluation as run_evaluation_direct
from autoresearch_problems.core.result import EvalResult
from autoresearch_problems.core.spec import ProblemSpec


# ── EvalResult.from_dict ──────────────────────────────────────────────────────

def test_eval_result_from_dict_full():
    d = {"score": 5.0, "valid": True, "error": "", "metrics": {"size": 5}}
    result = EvalResult.from_dict(d)
    assert result.score == 5.0
    assert result.valid is True
    assert result.error == ""
    assert result.metrics == {"size": 5}


def test_eval_result_from_dict_defaults():
    result = EvalResult.from_dict({})
    assert result.score == 0.0
    assert result.valid is False
    assert result.error == ""
    assert result.metrics == {}


def test_eval_result_from_dict_with_execution_time():
    d = {"score": 3.0, "valid": True, "execution_time": 0.5}
    result = EvalResult.from_dict(d)
    assert result.execution_time == 0.5


# ── run_evaluation: basic usage ───────────────────────────────────────────────

def test_run_evaluation_cap_set_valid():
    spec = registry.load("combinatorics/cap_set")
    S = np.array([[0, 0, 0, 0, 0, 0, 0, 0]])
    result = run_evaluation(spec, S)
    assert isinstance(result, EvalResult)
    assert result.valid
    assert result.score == 1.0
    assert result.execution_time >= 0.0


def test_run_evaluation_returns_eval_result_on_error():
    """A broken evaluator should return an invalid EvalResult, not raise."""
    spec = ProblemSpec(
        name="broken",
        category="test",
        description="",
        output_type="any",
        evaluator_code="def evaluate(output, **kw): raise RuntimeError('boom')",
        evaluator_entrypoint="evaluate",
        evaluator_dependencies=[],
        parameters={},
    )
    result = run_evaluation(spec, None)
    assert isinstance(result, EvalResult)
    assert not result.valid
    assert result.score == 0.0
    assert "boom" in result.error


def test_run_evaluation_missing_entrypoint():
    """Missing entrypoint function should return invalid result."""
    spec = ProblemSpec(
        name="bad",
        category="test",
        description="",
        output_type="any",
        evaluator_code="def wrong_name(output, **kw): return {'score': 1.0, 'valid': True, 'error': '', 'metrics': {}}",
        evaluator_entrypoint="evaluate",
        evaluator_dependencies=[],
        parameters={},
    )
    result = run_evaluation(spec, 42)
    assert not result.valid
    assert result.score == 0.0


def test_run_evaluation_kissing_number():
    """The icosahedron initial program should achieve score 12."""
    spec = registry.load("analysis/kissing_number")

    # Execute the initial_program source to get the solve() function
    ns: dict = {}
    exec(compile(spec.initial_program, "<initial_program>", "exec"), ns)  # noqa: S102
    centres = ns["solve"]()

    result = run_evaluation(spec, centres)
    assert result.valid
    assert result.score == 12.0


def test_run_evaluation_sets_execution_time():
    spec = registry.load("combinatorics/cap_set")
    S = np.array([[0, 0, 0, 0, 0, 0, 0, 0]])
    result = run_evaluation(spec, S)
    assert result.execution_time >= 0.0


# ── run_evaluation: parameters are passed correctly ───────────────────────────

def test_run_evaluation_passes_parameters():
    """Evaluator should receive spec.parameters as keyword args."""
    evaluator_code = """
def evaluate(output, expected=None, **kwargs):
    return {"score": float(output == expected), "valid": True, "error": "", "metrics": {}}
"""
    spec = ProblemSpec(
        name="param_test",
        category="test",
        description="",
        output_type="any",
        evaluator_code=evaluator_code,
        evaluator_entrypoint="evaluate",
        evaluator_dependencies=[],
        parameters={"expected": 42},
    )
    result = run_evaluation(spec, 42)
    assert result.valid
    assert result.score == 1.0

    result_wrong = run_evaluation(spec, 99)
    assert result_wrong.score == 0.0
