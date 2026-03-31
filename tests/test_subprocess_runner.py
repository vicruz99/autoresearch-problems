"""Tests for the SubprocessRunner."""

import subprocess
import sys

import numpy as np
import pytest

from autoresearch_problems.program_runners import SubprocessRunner


@pytest.fixture
def runner():
    return SubprocessRunner(timeout=30.0)


def test_subprocess_runner_simple_return(runner):
    code = "def add(): return 1 + 2"
    result = runner.execute(code, "add")
    assert result == 3


def test_subprocess_runner_returns_list(runner):
    code = "def make_list(): return [1, 2, 3]"
    result = runner.execute(code, "make_list")
    assert result == [1, 2, 3]


def test_subprocess_runner_numpy_array(runner):
    code = "import numpy as np\ndef make_array(): return np.array([1.0, 2.0, 3.0])"
    result = runner.execute(code, "make_array")
    np.testing.assert_array_equal(result, [1.0, 2.0, 3.0])


def test_subprocess_runner_raises_on_error(runner):
    code = "def boom(): raise ValueError('oops')"
    with pytest.raises(RuntimeError, match="oops"):
        runner.execute(code, "boom")


def test_subprocess_runner_timeout():
    slow_runner = SubprocessRunner(timeout=2.0)
    code = "import time\ndef sleep(): time.sleep(300)"
    with pytest.raises(subprocess.TimeoutExpired):
        slow_runner.execute(code, "sleep")


# ── Venv / python_executable support ─────────────────────────────────────────

def test_subprocess_runner_default_python():
    """With no arguments, runner should use sys.executable."""
    runner = SubprocessRunner()
    assert runner._python == sys.executable


def test_subprocess_runner_explicit_python_executable():
    """python_executable is stored and used directly."""
    runner = SubprocessRunner(python_executable="/usr/bin/python3")
    assert runner._python == "/usr/bin/python3"


def test_subprocess_runner_python_executable_takes_precedence(tmp_path):
    """python_executable wins over venv_path when both are given."""
    runner = SubprocessRunner(
        python_executable="/explicit/python",
        venv_path=str(tmp_path),
    )
    assert runner._python == "/explicit/python"


def test_subprocess_runner_venv_path_posix(tmp_path):
    """venv_path resolves to {venv}/bin/python on POSIX."""
    import os
    if os.name == "nt":
        pytest.skip("POSIX-only test")
    runner = SubprocessRunner(venv_path=str(tmp_path))
    assert runner._python == str(tmp_path / "bin" / "python")


def test_subprocess_runner_venv_path_windows(tmp_path, monkeypatch):
    """venv_path resolves to {venv}/Scripts/python.exe on Windows."""
    import os
    if os.name != "nt":
        pytest.skip("Windows-only test")
    runner = SubprocessRunner(venv_path=str(tmp_path))
    assert runner._python == str(tmp_path / "Scripts" / "python.exe")


# ── execute_batch ─────────────────────────────────────────────────────────────

def test_execute_batch_all_valid(runner):
    codes = [
        "def f(): return 1",
        "def f(): return 2",
        "def f(): return 3",
    ]
    results = runner.execute_batch(codes, function_name="f")
    assert results == [1, 2, 3]


def test_execute_batch_mixed_valid_invalid(runner):
    codes = [
        "def f(): return 42",
        "this is not valid python!!!",
        "def f(): return 99",
    ]
    results = runner.execute_batch(codes, function_name="f")
    assert results[0] == 42
    assert isinstance(results[1], Exception)
    assert results[2] == 99


def test_execute_batch_empty(runner):
    assert runner.execute_batch([], function_name="f") == []


def test_execute_batch_preserves_order(runner):
    """Results must be in the same order as input codes regardless of completion order."""
    codes = [f"def f(): return {i}" for i in range(10)]
    results = runner.execute_batch(codes, function_name="f")
    assert results == list(range(10))


def test_execute_batch_max_workers(runner):
    codes = ["def f(): return 1", "def f(): return 2"]
    results = runner.execute_batch(codes, function_name="f", max_workers=1)
    assert results == [1, 2]
