from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from autoresearch_problems.core.spec import ProblemSpec

# Root directory that contains all problem sub-directories
_PROBLEMS_ROOT = Path(__file__).parent.parent / "problems"


class Registry:
    """File-based problem registry.

    Problems live under ``problems/<category>/<name>/`` and each must contain
    a ``spec.yaml`` file plus an ``evaluator.py``.  Optional files
    ``initial_prompt.md`` and ``initial_program.py`` are loaded when present.
    """

    def __init__(self, problems_root: Path | None = None) -> None:
        self._root = problems_root or _PROBLEMS_ROOT

    # ── Discovery ─────────────────────────────────────────────────────────────

    def list_categories(self) -> list[str]:
        """Return sorted list of problem category names."""
        return sorted(
            p.name
            for p in self._root.iterdir()
            if p.is_dir() and not p.name.startswith("_")
        )

    def list_problems(self, category: str | None = None) -> list[str]:
        """Return ``["category/name", ...]`` for all (or filtered) problems."""
        results: list[str] = []
        search_root = self._root / category if category else self._root
        for spec_file in sorted(search_root.rglob("spec.yaml")):
            problem_dir = spec_file.parent
            rel = problem_dir.relative_to(self._root)
            results.append(str(rel))
        return results

    # ── Loading ───────────────────────────────────────────────────────────────

    def load(self, problem_id: str) -> ProblemSpec:
        """Load a :class:`ProblemSpec` from disk.

        *problem_id* is ``"category/name"`` (e.g. ``"combinatorics/cap_set"``).
        """
        problem_dir = self._root / problem_id
        if not problem_dir.is_dir():
            raise FileNotFoundError(
                f"Problem directory not found: {problem_dir}"
            )

        spec_path = problem_dir / "spec.yaml"
        if not spec_path.exists():
            raise FileNotFoundError(f"spec.yaml not found in {problem_dir}")

        with spec_path.open() as fh:
            raw: dict[str, Any] = yaml.safe_load(fh)

        evaluator_path = problem_dir / "evaluator.py"
        if not evaluator_path.exists():
            raise FileNotFoundError(f"evaluator.py not found in {problem_dir}")
        evaluator_code = evaluator_path.read_text()

        initial_prompt: str | None = None
        prompt_path = problem_dir / "initial_prompt.md"
        if prompt_path.exists():
            initial_prompt = prompt_path.read_text()

        initial_program: str | None = None
        program_path = problem_dir / "initial_program.py"
        if program_path.exists():
            initial_program = program_path.read_text()

        return ProblemSpec(
            name=raw["name"],
            category=raw["category"],
            description=raw.get("description", ""),
            function_name=raw.get("function_name", "solve"),
            output_type=raw.get("output_type", "any"),
            evaluator_code=evaluator_code,
            evaluator_entrypoint=raw.get("evaluator_entrypoint", "evaluate"),
            evaluator_dependencies=raw.get("evaluator_dependencies", []),
            parameters=raw.get("parameters", {}),
            timeout_seconds=float(raw.get("timeout_seconds", 30.0)),
            maximize=bool(raw.get("maximize", True)),
            known_best_score=raw.get("known_best_score"),
            initial_prompt=initial_prompt,
            initial_program=initial_program,
            source=raw.get("source", ""),
            tags=raw.get("tags", []),
        )


# Module-level singleton for convenience
registry = Registry()
