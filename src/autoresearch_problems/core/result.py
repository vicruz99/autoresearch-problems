from __future__ import annotations

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
