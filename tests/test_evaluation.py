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
    spec = registry.load("geometry/kissing_number_3d")

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


# ── run_evaluation_batch ──────────────────────────────────────────────────────

from autoresearch_problems.core.evaluation import run_evaluation_batch


def test_run_evaluation_batch_returns_correct_length():
    spec = registry.load("combinatorics/cap_set")
    outputs = [
        np.array([[0, 0, 0, 0, 0, 0, 0, 0]]),
        np.array([[1, 0, 0, 0, 0, 0, 0, 0]]),
        np.array([[2, 1, 0, 0, 0, 0, 0, 0]]),
    ]
    results = run_evaluation_batch(spec, outputs)
    assert len(results) == 3


def test_run_evaluation_batch_preserves_order():
    spec = registry.load("combinatorics/cap_set")
    # Two single-element outputs: scores should both be 1.0
    S1 = np.array([[0, 0, 0, 0, 0, 0, 0, 0]])
    S2 = np.array([[1, 0, 0, 0, 0, 0, 0, 0]])
    results = run_evaluation_batch(spec, [S1, S2])
    assert all(isinstance(r, EvalResult) for r in results)
    assert results[0].score == 1.0
    assert results[1].score == 1.0


def test_run_evaluation_batch_empty():
    spec = registry.load("combinatorics/cap_set")
    assert run_evaluation_batch(spec, []) == []


def test_run_evaluation_batch_handles_errors():
    """Invalid outputs should return invalid EvalResult, not raise."""
    spec = registry.load("combinatorics/cap_set")
    outputs = [None, np.array([[0, 0, 0, 0, 0, 0, 0, 0]])]
    results = run_evaluation_batch(spec, outputs)
    assert len(results) == 2
    assert not results[0].valid
    assert results[1].valid


def test_run_evaluation_batch_exported_from_init():
    from autoresearch_problems import run_evaluation_batch as rb
    assert callable(rb)


# ── run_evaluation: parameters kwarg ─────────────────────────────────────────

def test_run_evaluation_parameters_override():
    """parameters kwarg should override spec.parameters for the evaluator."""
    evaluator_code = """
def evaluate(output, n=8, **kwargs):
    return {"score": float(n), "valid": True, "error": "", "metrics": {}}
"""
    spec = ProblemSpec(
        name="param_override_test",
        category="test",
        description="",
        output_type="any",
        evaluator_code=evaluator_code,
        evaluator_entrypoint="evaluate",
        evaluator_dependencies=[],
        parameters={"n": 8},
    )
    result = run_evaluation(spec, None, parameters={"n": 20})
    assert result.valid
    assert result.score == 20.0


def test_run_evaluation_parameters_partial_override():
    """Partial parameters override merges with spec.parameters."""
    evaluator_code = """
def evaluate(output, n=1, q=1, **kwargs):
    return {"score": float(n + q), "valid": True, "error": "", "metrics": {}}
"""
    spec = ProblemSpec(
        name="partial_override_test",
        category="test",
        description="",
        output_type="any",
        evaluator_code=evaluator_code,
        evaluator_entrypoint="evaluate",
        evaluator_dependencies=[],
        parameters={"n": 8, "q": 3},
    )
    # Override only n; q should remain 3 from spec.parameters
    result = run_evaluation(spec, None, parameters={"n": 10})
    assert result.valid
    assert result.score == 13.0  # 10 + 3


def test_run_evaluation_parameters_none_unchanged():
    """Passing parameters=None should behave identically to not passing it."""
    spec = registry.load("combinatorics/cap_set")
    import numpy as np
    S = np.array([[0, 0, 0, 0, 0, 0, 0, 0]])
    result_default = run_evaluation(spec, S)
    result_none = run_evaluation(spec, S, parameters=None)
    assert result_default.valid == result_none.valid
    assert result_default.score == result_none.score


def test_run_evaluation_spec_not_mutated():
    """The spec.parameters dict must not be modified by run_evaluation()."""
    evaluator_code = """
def evaluate(output, n=1, **kwargs):
    return {"score": float(n), "valid": True, "error": "", "metrics": {}}
"""
    spec = ProblemSpec(
        name="immutable_test",
        category="test",
        description="",
        output_type="any",
        evaluator_code=evaluator_code,
        evaluator_entrypoint="evaluate",
        evaluator_dependencies=[],
        parameters={"n": 8},
    )
    run_evaluation(spec, None, parameters={"n": 99})
    assert spec.parameters["n"] == 8  # unchanged
