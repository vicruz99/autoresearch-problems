from dataclasses import dataclass, field
from typing import Any


@dataclass
class EvalResult:
    """The result of evaluating a candidate program's output."""

    score: float
    valid: bool
    execution_time: float = 0.0
    error: str = ""
    metrics: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: dict) -> "EvalResult":
        """Convert a plain dict (from an evaluator) to an EvalResult."""
        return cls(
            score=float(d.get("score", 0.0)),
            valid=bool(d.get("valid", False)),
            execution_time=float(d.get("execution_time", 0.0)),
            error=str(d.get("error", "")),
            metrics=dict(d.get("metrics", {})),
        )
