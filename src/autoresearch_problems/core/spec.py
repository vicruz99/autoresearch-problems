from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ProblemSpec:
    """The universal, framework-agnostic problem definition.

    A problem IS its evaluator.  Everything else (prompt, candidate program,
    candidate dependencies) is fluid and owned by the research framework.
    This dataclass is a **pure data container** — it has no methods that
    execute code.  Use :func:`~autoresearch_problems.core.evaluation.run_evaluation`
    to evaluate an output against this spec.
    """

    # ── Identity ──────────────────────────────────────────────────────────────
    name: str
    category: str
    description: str

    # ── Contract: what the evaluator expects ─────────────────────────────────
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
    function_name: str | None = None   # suggested function name (e.g. "solve")

    # ── Provenance ────────────────────────────────────────────────────────────
    source: str = ""
    tags: list[str] = field(default_factory=list)
