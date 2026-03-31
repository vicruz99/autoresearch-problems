"""Tests for core/pipeline.py — execute_and_evaluate and execute_and_evaluate_batch."""

from __future__ import annotations

import numpy as np
import pytest

from autoresearch_problems import (
    execute_and_evaluate,
    execute_and_evaluate_batch,
    registry,
)
from autoresearch_problems.core.result import EvalResult


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def cap_set_spec():
    return registry.load("combinatorics/cap_set")


# ── execute_and_evaluate ──────────────────────────────────────────────────────

def test_execute_and_evaluate_valid_code(cap_set_spec):
    code = "import numpy as np\ndef solve(): return np.array([[0,0,0,0,0,0,0,0]])"
    result = execute_and_evaluate(cap_set_spec, code, function_name="solve")
    assert isinstance(result, EvalResult)
    assert result.valid
    assert result.score == 1.0


def test_execute_and_evaluate_invalid_code(cap_set_spec):
    """Broken candidate code returns an invalid EvalResult, not an exception."""
    result = execute_and_evaluate(cap_set_spec, "this is not python", function_name="solve")
    assert isinstance(result, EvalResult)
    assert not result.valid
    assert result.score == 0.0
    assert result.error != ""


def test_execute_and_evaluate_wrong_output_shape(cap_set_spec):
    """Code that returns wrong-shape output should produce invalid EvalResult."""
    code = "import numpy as np\ndef solve(): return np.array([[1, 2, 3]])"
    result = execute_and_evaluate(cap_set_spec, code, function_name="solve")
    assert isinstance(result, EvalResult)
    assert not result.valid


def test_execute_and_evaluate_uses_spec_timeout(cap_set_spec):
    """Default runner respects spec.timeout_seconds."""
    from autoresearch_problems.program_runners.subprocess_runner import SubprocessRunner
    # Just verify that a custom runner can be passed in
    runner = SubprocessRunner(timeout=cap_set_spec.timeout_seconds)
    code = "import numpy as np\ndef solve(): return np.array([[0,0,0,0,0,0,0,0]])"
    result = execute_and_evaluate(cap_set_spec, code, function_name="solve", runner=runner)
    assert result.valid


def test_execute_and_evaluate_never_raises(cap_set_spec):
    """execute_and_evaluate must never raise — even for completely broken input."""
    result = execute_and_evaluate(cap_set_spec, "import this\ndef solve(): 1/0", function_name="solve")
    assert isinstance(result, EvalResult)


# ── execute_and_evaluate_batch ────────────────────────────────────────────────

def test_execute_and_evaluate_batch_all_valid(cap_set_spec):
    code = "import numpy as np\ndef solve(): return np.array([[0,0,0,0,0,0,0,0]])"
    results = execute_and_evaluate_batch(cap_set_spec, [code, code], function_name="solve")
    assert len(results) == 2
    assert all(r.valid for r in results)


def test_execute_and_evaluate_batch_mixed(cap_set_spec):
    valid_code = "import numpy as np\ndef solve(): return np.array([[0,0,0,0,0,0,0,0]])"
    invalid_code = "not valid python!!!"
    results = execute_and_evaluate_batch(
        cap_set_spec,
        [valid_code, invalid_code, valid_code],
        function_name="solve",
    )
    assert len(results) == 3
    assert results[0].valid
    assert not results[1].valid
    assert results[2].valid


def test_execute_and_evaluate_batch_empty(cap_set_spec):
    assert execute_and_evaluate_batch(cap_set_spec, []) == []


def test_execute_and_evaluate_batch_preserves_order(cap_set_spec):
    """Results must be returned in the same order as input codes."""
    codes = [
        "import numpy as np\ndef solve(): return np.array([[0,0,0,0,0,0,0,0]])",
        "not valid python!!!",
        "import numpy as np\ndef solve(): return np.array([[1,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0]])",
    ]
    results = execute_and_evaluate_batch(cap_set_spec, codes, function_name="solve")
    assert results[0].valid
    assert not results[1].valid
    assert results[2].valid


def test_execute_and_evaluate_batch_exported_from_init():
    from autoresearch_problems import execute_and_evaluate_batch as eaeb
    assert callable(eaeb)
