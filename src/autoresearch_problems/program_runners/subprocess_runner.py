"""Subprocess-based program runner.

Executes untrusted LLM-generated code in an isolated subprocess and returns
the result of calling a named function.  Communication uses pickle (via a
temporary file) so arbitrary Python objects can be exchanged.

Inspired by the subprocess/pickle pattern in
``YonatanGideoni/code_evo_simple_baselines``'s
``BaseEvaluator._run_algorithm_with_timeout()``.
"""

from __future__ import annotations

import concurrent.futures
import os
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

    The caller's Python interpreter is reused by default so the candidate code
    runs in a compatible environment.  An optional *venv_path* or
    *python_executable* parameter allows running code in a custom virtual
    environment.  A temporary directory is used for the script and the IPC
    pickle file.

    Parameters
    ----------
    timeout:
        Maximum wall-clock seconds to wait for the subprocess.
    python_executable:
        Explicit path to a Python binary to use (e.g. ``/usr/bin/python3.11``).
        Takes precedence over *venv_path*.
    venv_path:
        Path to a virtual-environment directory.  The runner will resolve the
        Python binary automatically (``{venv_path}/bin/python`` on POSIX,
        ``{venv_path}/Scripts/python.exe`` on Windows).
    """

    def __init__(
        self,
        timeout: float = 30.0,
        python_executable: str | None = None,
        venv_path: str | None = None,
    ) -> None:
        self.timeout = timeout

        if python_executable is not None:
            self._python = python_executable
        elif venv_path is not None:
            venv = Path(venv_path)
            if os.name == "nt":
                self._python = str(venv / "Scripts" / "python.exe")
            else:
                self._python = str(venv / "bin" / "python")
        else:
            self._python = sys.executable

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
                    [self._python, str(script_path)],
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

    def execute_batch(
        self,
        codes: list[str],
        function_name: str,
        max_workers: int | None = None,
    ) -> list[Any | Exception]:
        """Execute multiple candidate programs in parallel.

        Each candidate is executed in its own subprocess via
        :meth:`execute`.  Failures are caught and returned as
        :class:`Exception` objects rather than raised, so the list always
        has the same length as *codes*.

        Uses :class:`concurrent.futures.ThreadPoolExecutor` — threads are
        sufficient because each ``execute()`` call already spawns a
        subprocess; the threads only wait for I/O.

        Parameters
        ----------
        codes:
            List of candidate source code strings.
        function_name:
            Name of the zero-argument function defined in each code string.
        max_workers:
            Maximum number of parallel workers.  Defaults to
            ``min(len(codes), (os.cpu_count() or 1) * 4)``.

        Returns
        -------
        list[Any | Exception]
            Results in the same order as *codes*.  Entries are the return
            value of ``function_name()`` on success, or an
            :class:`Exception` instance on failure.
        """
        if not codes:
            return []

        collected: dict[int, Any | Exception] = {}

        def _run(index: int, code: str) -> tuple[int, Any | Exception]:
            try:
                return index, self.execute(code, function_name)
            except Exception as exc:  # noqa: BLE001
                return index, exc

        workers = max_workers or min(len(codes), (os.cpu_count() or 1) * 4)
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
            futures = [pool.submit(_run, i, c) for i, c in enumerate(codes)]
            for future in concurrent.futures.as_completed(futures):
                idx, value = future.result()
                collected[idx] = value

        return [collected[i] for i in range(len(codes))]
