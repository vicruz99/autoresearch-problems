"""Subprocess-based program runner.

Executes untrusted LLM-generated code in an isolated subprocess and returns
the result of calling a named function.  Communication uses pickle (via a
temporary file) so arbitrary Python objects can be exchanged.

Inspired by the subprocess/pickle pattern in
``YonatanGideoni/code_evo_simple_baselines``'s
``BaseEvaluator._run_algorithm_with_timeout()``.
"""

from __future__ import annotations

import pickle
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

# Wrapper template written to a temp script file.  No leading whitespace so
# that embedding arbitrary user code never causes IndentationError.
_WRAPPER_TEMPLATE = """\
import pickle as _pickle
import sys as _sys

{code}

try:
    _result = {function_name}()
    with open({result_path!r}, "wb") as _fh:
        _pickle.dump(_result, _fh)
except Exception as _exc:
    with open({result_path!r}, "wb") as _fh:
        _pickle.dump(_exc, _fh)
    _sys.exit(1)
"""


class SubprocessRunner:
    """Run code in a subprocess, call *function_name*(), return the result.

    The caller's Python interpreter is reused so the candidate code runs in a
    compatible environment.  A temporary directory is used for the script and
    the IPC pickle file.

    Parameters
    ----------
    timeout:
        Maximum wall-clock seconds to wait for the subprocess.
    """

    def __init__(self, timeout: float = 30.0) -> None:
        self.timeout = timeout

    def execute(self, code: str, function_name: str) -> Any:
        """Execute *code* in a subprocess and return ``function_name()``.

        Raises
        ------
        subprocess.TimeoutExpired
            If the subprocess does not finish within *self.timeout* seconds.
        RuntimeError
            If the subprocess exits with a non-zero status.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            script_path = tmp_path / "runner_script.py"
            result_path = tmp_path / "result.pkl"

            wrapper = _WRAPPER_TEMPLATE.format(
                code=code,
                function_name=function_name,
                result_path=str(result_path),
            )

            script_path.write_text(wrapper)

            try:
                proc = subprocess.run(
                    [sys.executable, str(script_path)],
                    capture_output=True,
                    timeout=self.timeout,
                )
            except subprocess.TimeoutExpired:
                raise

            if not result_path.exists():
                raise RuntimeError(
                    f"Subprocess exited with code {proc.returncode} and produced "
                    f"no output.\nstderr: {proc.stderr.decode()}"
                )

            with result_path.open("rb") as fh:
                payload = pickle.load(fh)  # noqa: S301

            if proc.returncode != 0:
                raise RuntimeError(
                    f"Subprocess raised: {payload}\nstderr: {proc.stderr.decode()}"
                )

            return payload
