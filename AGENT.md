# Copilot Instructions — autoresearch-problems

## Project overview

`autoresearch-problems` is a **universal, framework-agnostic** Python library of benchmark problems for LLM-driven automated research and program-evolution frameworks (FunSearch, AlphaEvolve, ShinkaEvolve, OpenEvolve, BLADE, etc.).

**Core philosophy: a problem IS its evaluator.** The evaluator is fixed and owned by this library. Everything else — the LLM prompt, the candidate program, the candidate's dependencies — is fluid and owned by the research framework that consumes this library.

## Repository layout

```
src/autoresearch_problems/
├── __init__.py                          # Public API re-exports
├── core/
│   ├── __init__.py
│   ├── spec.py          # ProblemSpec  (frozen dataclass, pure data)
│   ├── result.py        # EvalResult   (dataclass)
│   ├── evaluation.py    # run_evaluation(), run_evaluation_batch()
│   ├── pipeline.py      # execute_and_evaluate(), execute_and_evaluate_batch()
│   └── registry.py      # Registry class + module-level `registry` singleton
├── problems/
│   ├── __init__.py
│   ├── analysis/        # e.g. kissing_number/
│   ├── combinatorics/   # e.g. cap_set/
│   └── geometry/        # e.g. circle_packing/
└── program_runners/
    ├── __init__.py
    └── subprocess_runner.py   # SubprocessRunner (subprocess + pickle IPC)

tests/
├── test_evaluation.py
├── test_evaluators.py
├── test_pipeline.py
├── test_registry.py
└── test_subprocess_runner.py

notebooks/
└── quickstart.ipynb
```

## Coding style & conventions

- Use `dataclasses` (not Pydantic) for data containers.
- `ProblemSpec` is a **frozen** dataclass — never add methods that execute code to it.
- Evaluator files (`evaluator.py`) must be **completely standalone**: they must NOT import from `autoresearch_problems`. Their only allowed dependencies are those listed in `evaluator_dependencies` (typically just `numpy`).
- All public API is re-exported from `src/autoresearch_problems/__init__.py`.

## Key data models

### `ProblemSpec` (frozen dataclass in `core/spec.py`)

| Field | Type | Purpose |
|---|---|---|
| `name` | `str` | Problem identifier (e.g. `"cap_set"`) |
| `category` | `str` | Category slug (e.g. `"combinatorics"`) |
| `description` | `str` | Human-readable description |
| `output_type` | `str` | Expected output type hint (e.g. `"numpy_array"`) |
| `evaluator_code` | `str` | Full source code of the standalone evaluator |
| `evaluator_entrypoint` | `str` | Function name to call (usually `"evaluate"`) |
| `evaluator_dependencies` | `list[str]` | Pinned pip deps the evaluator needs |
| `parameters` | `dict[str, Any]` | Kwargs passed to the evaluator |
| `timeout_seconds` | `float` | Default 30.0 |
| `maximize` | `bool` | True = higher score is better |
| `known_best_score` | `float \| None` | Known optimum (if any) |
| `initial_prompt` | `str \| None` | Suggested LLM prompt |
| `initial_program` | `str \| None` | Seed solution code |
| `function_name` | `str \| None` | Suggested function name (e.g. `"solve"`) |
| `source` | `str` | Provenance URL or paper reference |
| `tags` | `list[str]` | Searchable tags |

### `EvalResult` (dataclass in `core/result.py`)

| Field | Type |
|---|---|
| `score` | `float` |
| `valid` | `bool` |
| `execution_time` | `float` |
| `error` | `str` |
| `metrics` | `dict[str, Any]` |

## Adding a new problem

Every problem lives in its own directory: `src/autoresearch_problems/problems/<category>/<name>/`

### Required files

1. **`spec.yaml`** — metadata (name, category, description, output_type, evaluator_entrypoint, evaluator_dependencies, parameters, timeout_seconds, maximize, known_best_score, source, tags).
2. **`evaluator.py`** — standalone Python file that defines an `evaluate(output, **params) -> dict` function. Must NOT import from `autoresearch_problems`. Must return a dict with keys: `score`, `valid`, `error`, `metrics`.

### Optional files

3. **`initial_prompt.md`** — suggested LLM prompt for frameworks.
4. **`initial_program.py`** — seed solution defining a zero-argument function (usually `solve()`).

### Evaluator contract

```python
def evaluate(output: Any, **kwargs) -> dict:
    """
    Returns:
        {
            "score": float,       # primary metric
            "valid": bool,        # does the output satisfy constraints?
            "error": str,         # "" on success, error message on failure
            "metrics": dict,      # any extra info
        }
    """
```

- The evaluator must **never raise**; catch all exceptions internally and return `valid=False` with an error message.
- The evaluator receives the raw output object and the `parameters` from `spec.yaml` as kwargs.

### Checklist when adding a problem

- [ ] Create `problems/<category>/<name>/` directory
- [ ] Add `spec.yaml` with all required fields
- [ ] Add `evaluator.py` — standalone, no `autoresearch_problems` imports
- [ ] (Optional) Add `initial_prompt.md` and `initial_program.py` and `function_name`
- [ ] Add tests in `tests/test_evaluators.py` covering: valid output, invalid output, edge cases
- [ ] Verify `registry.list_problems()` discovers the new problem
- [ ] Update the Problem Catalog table in `README.md`

## Problem sources to port

These are known sources of benchmark problems used across the automated research ecosystem. When porting a problem, set the `source` field in `spec.yaml` to the original repo/paper URL.

| Source | Repo / Reference | Example problems |
|---|---|---|
| FunSearch (DeepMind) | `google-deepmind/funsearch` | Cap set, online bin packing, admissible sets |
| AlphaEvolve (DeepMind) | AlphaEvolve paper + BLADE integration | Kissing number, circle packing, matrix multiplication, Fourier analysis |
| ShinkaEvolve (Sakana AI) | `SakanaAI/ShinkaEvolve` | Circle packing, AIME math, competitive programming |
| OpenEvolve | `codelion/openevolve` | GPU kernel optimization, numerical algorithms |
| BLADE | `XAI-liacs/BLADE` | BBOB, SBOX-COST, MA-BBOB, photonics, AlphaEvolve benchmarks |
| code_evo_simple_baselines | `YonatanGideoni/code_evo_simple_baselines` | Short/long/variant problems in `baselines/problems/` |

## Execution model

```
┌──────────────────────────────┐     ┌──────────────────────────────┐
│     PROGRAM SANDBOX          │     │     EVALUATOR SANDBOX        │
│                              │     │                              │
│  LLM-generated code          │     │  Fixed evaluator code        │
│  Unknown/changing deps       │     │  Known, stable deps          │
│  Owned by: research framework│     │  Owned by: this library      │
│                              │     │                              │
│  SubprocessRunner.execute()  │────▶│  run_evaluation(spec, output)│
│  Returns raw output          │     │  Returns EvalResult          │
└──────────────────────────────┘     └──────────────────────────────┘
```

- **`SubprocessRunner`** executes untrusted code in an isolated subprocess using pickle IPC. It supports custom `python_executable` or `venv_path` for environment isolation.
- **`run_evaluation()`** dynamically loads the evaluator via `exec()` in a fresh namespace. Never raises — always returns `EvalResult`.
- **`execute_and_evaluate()`** combines both steps as a convenience.
- **Batch variants** (`run_evaluation_batch`, `execute_and_evaluate_batch`, `SubprocessRunner.execute_batch`) use `ThreadPoolExecutor` for parallelism.

## Testing

- Use `pytest` for all tests.
- Test files live in `tests/`.
- Every evaluator should have tests in `test_evaluators.py` with valid, invalid, and edge-case outputs.
- Pipeline and integration tests go in `test_pipeline.py`.
- Tests must not require network access or GPU.
- Run tests with: `pip install -e ".[dev]" && pytest`

## Dependencies

- **Core:** `pyyaml>=6.0`, `numpy>=1.24` (required)
- **Runners extra:** `cloudpickle>=3.0` (optional: `pip install "autoresearch-problems[runners]"`)
- **Dev:** `pytest>=7.0`, `cloudpickle>=3.0`

## Things to avoid

- Do NOT add methods to `ProblemSpec` that execute code — it is a pure data container.
- Do NOT import `autoresearch_problems` inside evaluator files.
- Do NOT use Pydantic or attrs — stick with stdlib `dataclasses`.
- Do NOT add heavy dependencies to the core library; evaluator-specific deps go in `evaluator_dependencies`.
- Do NOT break the `evaluate(output, **kwargs) -> dict` contract.
- Do NOT use `typing.Union` — use `X | Y` syntax (Python 3.10+).