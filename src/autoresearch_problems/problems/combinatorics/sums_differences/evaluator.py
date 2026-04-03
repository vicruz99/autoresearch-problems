"""Evaluator for the Sums and Differences (Ruzsa's inequality) problem.

Matches the scoring from sums_differences_problems.ipynb Cell 5:
  n_unique = len(set(A))
  lhs = |A-A| / n_unique
  rhs = |A+A| / n_unique
  score = log(rhs) / log(lhs) + (1 - 1/n_unique) / 100
"""
import math


def evaluate(output: object, **kwargs) -> dict:
    try:
        lst = [int(x) for x in output]
    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}
    if len(lst) < 2:
        return {"score": 0.0, "valid": False,
                "error": "Need at least 2 elements", "metrics": {}}

    lst_set = set(lst)
    if len(lst_set) < 2:
        return {"score": 0.0, "valid": False,
                "error": "Elements must be distinct", "metrics": {}}

    # Check for values that are too large
    for x in lst_set:
        if abs(x) > 2_000_000_000:
            return {"score": 0.0, "valid": False,
                    "error": f"Element {x} exceeds 2_000_000_000", "metrics": {}}

    n_unique = len(lst_set)

    a_minus_a = set(i - j for i in lst_set for j in lst_set)
    a_plus_a = set(i + j for i in lst_set for j in lst_set)

    lhs = len(a_minus_a) / n_unique   # |A-A| / |A|
    rhs = len(a_plus_a) / n_unique    # |A+A| / |A|

    if lhs <= 1.0 or rhs <= 1.0:
        return {"score": 0.0, "valid": False,
                "error": "log base would be <= 1", "metrics": {}}

    try:
        # Match notebook Cell 5: log(rhs) / log(lhs) + (1 - 1/n_unique) / 100
        score = math.log(rhs) / math.log(lhs) + (1.0 - 1.0 / n_unique) / 100.0
    except (ZeroDivisionError, ValueError) as exc:
        return {"score": 0.0, "valid": False,
                "error": f"Cannot compute log ratio: {exc}", "metrics": {}}

    return {"score": score, "valid": True, "error": "",
            "metrics": {"size_A": n_unique, "|A-A|": len(a_minus_a), "|A+A|": len(a_plus_a),
                        "lhs": lhs, "rhs": rhs}}
