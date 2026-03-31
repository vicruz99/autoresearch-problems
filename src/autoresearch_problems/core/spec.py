from __future__ import annotations

import traceback
import types
from dataclasses import dataclass, field
from typing import Any

from autoresearch_problems.core.result import EvalResult


@dataclass(frozen=True)
class ProblemSpec:
    """The universal, framework-agnostic problem definition.

    A problem IS its evaluator.  Everything else (prompt, candidate program,
    candidate dependencies) is fluid and owned by the research framework.
    This dataclass owns the evaluator contract and static metadata.
    """

    # ── Identity ──────────────────────────────────────────────────────────────
    name: str
    category: str
    description: str

    # ── Contract: what the evaluator expects ─────────────────────────────────
    function_name: str       # function the candidate program must expose
    output_type: str         # e.g. "numpy_array", "list[int]", "float"

    # ── Evaluator (source + entrypoint) ───────────────────────────────────────
    evaluator_code: str          # full source code of the evaluator module
    evaluator_entrypoint: str    # function name inside evaluator_code to call
    evaluator_dependencies: list[str]  # pinned deps the evaluator needs

    # ── Evaluator parameters ──────────────────────────────────────────────────
    parameters: dict[str, Any]
    timeout_seconds: float = 30.0
    maximize: bool = True
    known_best_score: float | None = None

    # ── Optional hints for frameworks ────────────────────────────────────────
    initial_prompt: str | None = None
    initial_program: str | None = None

    # ── Provenance ────────────────────────────────────────────────────────────
    source: str = ""
    tags: list[str] = field(default_factory=list)

    def evaluate(self, output: Any) -> EvalResult:
        """Convenience: dynamically load the evaluator and score *output*.

        The evaluator entrypoint is called as::

            result = <entrypoint>(output, **self.parameters)

        The entrypoint must return either an :class:`EvalResult` or a plain
        ``float``/``int`` (which is wrapped in a valid :class:`EvalResult`).

        Any exception raised by the evaluator is caught and returned as an
        invalid :class:`EvalResult` with ``score=0.0``.
        """
        try:
            module = types.ModuleType("_evaluator")
            exec(compile(self.evaluator_code, "<evaluator>", "exec"), module.__dict__)  # noqa: S102
            entrypoint = getattr(module, self.evaluator_entrypoint)
            raw = entrypoint(output, **self.parameters)
            if isinstance(raw, EvalResult):
                return raw
            return EvalResult(score=float(raw), valid=True)
        except Exception:
            return EvalResult(
                score=0.0,
                valid=False,
                error=traceback.format_exc(),
            )
