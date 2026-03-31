"""End-to-end pipeline helpers: execute candidate code and evaluate it."""

from __future__ import annotations

import concurrent.futures
import os
from typing import TYPE_CHECKING, Any

from autoresearch_problems.core.evaluation import run_evaluation
from autoresearch_problems.core.result import EvalResult
from autoresearch_problems.core.spec import ProblemSpec

if TYPE_CHECKING:
    from autoresearch_problems.program_runners.subprocess_runner import SubprocessRunner


def execute_and_evaluate(
    spec: ProblemSpec,
    code: str,
    function_name: str = "solve",
    runner: SubprocessRunner | None = None,
) -> EvalResult:
    """Execute candidate code in a subprocess, then evaluate the output.

    Convenience function that combines
    :meth:`~autoresearch_problems.program_runners.SubprocessRunner.execute`
    and :func:`~autoresearch_problems.core.evaluation.run_evaluation`.

    Parameters
    ----------
    spec:
        The :class:`ProblemSpec` to evaluate against.
    code:
        Candidate source code string.  Must define a zero-argument function
        named *function_name*.
    function_name:
        Name of the function to call inside *code*.  Defaults to ``"solve"``.
    runner:
        :class:`~autoresearch_problems.program_runners.SubprocessRunner` to
        use.  If ``None``, a default runner is created with
        ``timeout=spec.timeout_seconds``.

    Returns
    -------
    EvalResult
        Always returns an :class:`EvalResult`; never raises.
    """
    from autoresearch_problems.program_runners.subprocess_runner import SubprocessRunner as _Runner

    if runner is None:
        runner = _Runner(timeout=spec.timeout_seconds)

    try:
        output = runner.execute(code, function_name)
    except Exception as exc:  # noqa: BLE001
        return EvalResult(score=0.0, valid=False, error=str(exc))

    return run_evaluation(spec, output)


def execute_and_evaluate_batch(
    spec: ProblemSpec,
    codes: list[str],
    function_name: str = "solve",
    runner: SubprocessRunner | None = None,
    max_workers: int | None = None,
) -> list[EvalResult]:
    """Execute and evaluate multiple candidates in parallel.

    Each candidate is executed in a subprocess (via
    :func:`execute_and_evaluate`) and then evaluated against *spec*.  Uses
    :class:`concurrent.futures.ThreadPoolExecutor` for parallelism since each
    execution already spawns its own subprocess.

    Parameters
    ----------
    spec:
        The :class:`ProblemSpec` to evaluate against.
    codes:
        List of candidate source code strings.
    function_name:
        Name of the function to call inside each code string.
    runner:
        :class:`~autoresearch_problems.program_runners.SubprocessRunner` to
        use.  If ``None``, a default runner is created with
        ``timeout=spec.timeout_seconds``.
    max_workers:
        Maximum number of parallel workers.  Defaults to
        ``min(len(codes), (os.cpu_count() or 1) * 4)``.

    Returns
    -------
    list[EvalResult]
        Results in the same order as *codes*.  Failed executions return
        ``EvalResult(score=0, valid=False, error=...)``.
    """
    if not codes:
        return []

    from autoresearch_problems.program_runners.subprocess_runner import SubprocessRunner as _Runner

    if runner is None:
        runner = _Runner(timeout=spec.timeout_seconds)

    collected: dict[int, EvalResult] = {}

    def _run(index: int, code: str) -> tuple[int, EvalResult]:
        return index, execute_and_evaluate(spec, code, function_name, runner)

    workers = max_workers or min(len(codes), (os.cpu_count() or 1) * 4)
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(_run, i, c) for i, c in enumerate(codes)]
        for future in concurrent.futures.as_completed(futures):
            idx, value = future.result()
            collected[idx] = value

    return [collected[i] for i in range(len(codes))]
