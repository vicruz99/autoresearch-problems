"""Evaluator for the Sums and Differences (Ruzsa's inequality) problem."""
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

    a_minus_a = set(i - j for i in lst_set for j in lst_set)
    a_plus_a = set(i + j for i in lst_set for j in lst_set)

    size_diff = len(a_minus_a)
    size_sum = len(a_plus_a)

    if size_sum <= 1:
        return {"score": 0.0, "valid": False,
                "error": "A+A has fewer than 2 elements", "metrics": {}}

    try:
        score = math.log(size_diff) / math.log(size_sum)
    except (ZeroDivisionError, ValueError) as exc:
        return {"score": 0.0, "valid": False,
                "error": f"Cannot compute log ratio: {exc}", "metrics": {}}

    return {"score": score, "valid": True, "error": "",
            "metrics": {"size_A": len(lst_set), "|A-A|": size_diff, "|A+A|": size_sum}}
