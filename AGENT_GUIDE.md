# Agent Guide — autoresearch-problems

This guide is for LLM agents (AlphaEvolve, FunSearch, OpenEvolve, ShinkaEvolve, BLADE, etc.) consuming this library.

## Quick Start

```python
from autoresearch_problems import registry

# List all problems
registry.list_problems()

# Load a problem spec
spec = registry.load("combinatorics/cap_set")
print(spec.description)         # human-readable description
print(spec.initial_prompt)      # suggested LLM prompt for this problem
print(spec.initial_program)     # seed solution to start from
print(spec.parameters)          # problem parameters (n, p, etc.)
print(spec.maximize)            # True = higher score is better
print(spec.known_best_score)    # None if open, float if known
```

## Writing a Candidate Program

Your `solve` function must:

1. Match the function name in `spec.function_name` (always `solve`).
2. Accept keyword arguments matching `spec.parameters`.
3. Return an output matching `spec.output_type`.

```python
# Example: cap_set (output_type = numpy_array, parameters = {n: 8, q: 3})
import numpy as np

def solve(n: int = 8, q: int = 3) -> np.ndarray:
    # Return an array of shape (k, n) with entries in {0, ..., q-1}
    # representing a set of k vectors in F_q^n
    return np.array([[0]*n, [1,0,0,0,0,0,0,0]])
```

## Running Your Program

```python
# Option A: call solve() directly and pass output to evaluate
output = solve(**spec.parameters)
result = spec.evaluate(output)
print(result.score, result.valid, result.error)

# Option B: use the SubprocessRunner for isolation
from autoresearch_problems.program_runners import SubprocessRunner
runner = SubprocessRunner(timeout=30.0)
output = runner.execute(code=candidate_code, function_name=spec.function_name)
result = spec.evaluate(output)
```

## The `evaluate()` Contract

```python
result = spec.evaluate(output)
# result.score   : float  — primary metric; higher is better if spec.maximize=True
# result.valid   : bool   — False if output violates hard constraints
# result.error   : str    — non-empty if an exception occurred during evaluation
# result.metrics : dict   — optional extra metrics (problem-specific)
```

- When `result.valid = False`, `result.score` is typically `-inf` or `0.0`.
- When `result.error` is non-empty, your program either crashed or returned wrong types.
- The evaluator is deterministic and fixed — you cannot modify it.

## Output Type Descriptions

| `output_type` | Python type | Notes |
|---|---|---|
| `numpy_array` | `np.ndarray` | Shape and dtype vary by problem; check evaluator.py |
| `list` | `list` | May be list of floats, ints, or nested lists |
| `list[float]` | `list[float]` | Flat list of floats |
| `list[int]` | `list[int]` | Flat list of integers |
| `callable` | `Callable` | A function object; used in online_bin_packing |
| `dict` | `dict` | A dictionary; used in prime_number_theorem |

For `numpy_array`, the evaluator will call `np.asarray()` on your output, so returning a Python list of lists also works.

## Iterating and Improving Scores

1. **Start from `spec.initial_program`** — it is a working baseline.
2. **Check `spec.maximize`** before interpreting scores: for minimize problems, a lower score is better.
3. **Compare to `spec.known_best_score`** — scores beyond this are new records.
4. **Use `result.metrics`** — many evaluators expose intermediate quantities useful for debugging.
5. **Small changes first** — mutate the baseline program rather than generating from scratch.
6. **Watch for `valid=False`** — fix hard constraint violations before optimizing the score.

### Evolutionary loop sketch

```python
best_score = -float('inf') if spec.maximize else float('inf')
best_program = spec.initial_program

for iteration in range(max_iters):
    candidate_code = llm_mutate(best_program)
    try:
        output = run_in_sandbox(candidate_code, spec.parameters)
        result = spec.evaluate(output)
        if result.valid and is_better(result.score, best_score, spec.maximize):
            best_score = result.score
            best_program = candidate_code
    except Exception:
        pass  # invalid program, skip
```

## Common Pitfalls

- **Wrong output shape**: most `numpy_array` problems expect shape `(n, d)` — read the evaluator or initial program carefully.
- **Returning `None`**: if `solve()` returns `None`, `evaluate()` will raise an error with `valid=False`.
- **Ignoring parameter defaults**: always accept `**kwargs` or match parameter names exactly; the evaluator passes `spec.parameters` as keyword arguments.
- **Forgetting normalization**: many scoring functions divide by a reference — outputs need to be normalized before the score is meaningful.
- **Timeout**: `spec.timeout_seconds` is the wall-clock budget. Use vectorized NumPy operations; avoid Python loops over large arrays.
- **Callable output**: for `online_bin_packing`, your `solve()` must **return a function** (heuristic), not a value.
