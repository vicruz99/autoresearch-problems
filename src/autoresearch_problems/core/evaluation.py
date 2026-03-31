"""Evaluation utility: run_evaluation(spec, output) -> EvalResult."""

from __future__ import annotations

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
