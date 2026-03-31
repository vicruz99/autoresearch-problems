"""Tests for the SubprocessRunner."""

import subprocess

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
