"""Evaluation utility: run_evaluation(spec, output) -> EvalResult."""

from __future__ import annotations

import concurrent.futures
import os
import time
from typing import Any

from autoresearch_problems.core.result import EvalResult
from autoresearch_problems.core.spec import ProblemSpec


def run_evaluation(spec: ProblemSpec, output: Any) -> EvalResult:
    """Load the evaluator from *spec* and run it on *output*.

    1. Dynamically loads the evaluator source code into a fresh namespace.
    2. Calls ``spec.evaluator_entrypoint(output, **spec.parameters)``.
    3. Converts the returned ``dict`` to an :class:`EvalResult`.
    4. Handles all exceptions gracefully, returning an invalid result.

    Parameters
    ----------
    spec:
        The :class:`ProblemSpec` whose evaluator to run.
    output:
        The candidate output to evaluate.

    Returns
    -------
    EvalResult
        Always returns an :class:`EvalResult`; never raises.
    """
    start = time.monotonic()
    try:
        namespace: dict[str, Any] = {}
        exec(compile(spec.evaluator_code, "<evaluator>", "exec"), namespace)  # noqa: S102
        eval_fn = namespace[spec.evaluator_entrypoint]
        result_dict = eval_fn(output, **spec.parameters)
        result = EvalResult.from_dict(result_dict)
        return EvalResult(
            score=result.score,
            valid=result.valid,
            execution_time=time.monotonic() - start,
            error=result.error,
            metrics=result.metrics,
        )
    except Exception as exc:
        return EvalResult(
            score=0.0,
            valid=False,
            execution_time=time.monotonic() - start,
            error=str(exc),
        )


def run_evaluation_batch(
    spec: ProblemSpec,
    outputs: list[Any],
    max_workers: int | None = None,
) -> list[EvalResult]:
    """Evaluate multiple outputs against the same spec in parallel.

    Uses :class:`concurrent.futures.ThreadPoolExecutor`.  Each evaluation is
    independent and calls :func:`run_evaluation` which never raises.

    Parameters
    ----------
    spec:
        The :class:`ProblemSpec` to evaluate against.
    outputs:
        List of candidate outputs to evaluate.
    max_workers:
        Maximum number of parallel workers.  Defaults to
        ``min(len(outputs), (os.cpu_count() or 1) * 4)``.

    Returns
    -------
    list[EvalResult]
        Results in the same order as *outputs*.
    """
    if not outputs:
        return []

    collected: dict[int, EvalResult] = {}

    def _eval(index: int, output: Any) -> tuple[int, EvalResult]:
        return index, run_evaluation(spec, output)

    workers = max_workers or min(len(outputs), (os.cpu_count() or 1) * 4)
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(_eval, i, o) for i, o in enumerate(outputs)]
        for future in concurrent.futures.as_completed(futures):
            idx, value = future.result()
            collected[idx] = value

    return [collected[i] for i in range(len(outputs))]
