# Verification Tiers

When an automated research agent improves a benchmark score, not all improvements are equally trustworthy. This document defines four tiers of verification for solutions produced by agents running against `autoresearch-problems`.

## Tier 0 — Score Improvement (Numerical)

**Definition**: The evaluator returns a better score than any previously recorded score.

**Requirements**:
- `result.valid = True`
- `result.score` strictly beats `spec.known_best_score`

**Trust level**: Low. The score is real but the result may be a numerical artefact, overfitting to the evaluator, or non-generalizing.

**Example**: A candidate program finds a ±1 polynomial with L∞ norm 1.381 on the unit circle for `flat_polynomials` — beating the known 1.384 record.

---

## Tier 1 — Reproducible Score

**Definition**: The solution can be re-run independently, the code is readable, and the score is reproducible across multiple runs and machines.

**Requirements**:
- Tier 0 satisfied
- Candidate code is self-contained and runs without modification
- Score is stable across ≥3 independent evaluations
- No use of random seeds that make the result non-reproducible

**Trust level**: Medium. The result is likely genuine but may still be a narrow construction that does not generalize.

**Example**: A Kakeya construction for `finite_field_kakeya/d3` that can be run with `python initial_program.py` and consistently outputs the same improved score.

---

## Tier 2 — Mathematical Verification

**Definition**: A human mathematician has reviewed the construction and confirmed it is mathematically valid (not just numerically valid).

**Requirements**:
- Tier 1 satisfied
- Human-written proof sketch explaining why the construction achieves the claimed score
- Proof sketch reviewed and confirmed by at least one mathematician
- Construction generalizes beyond the specific parameter instance tested

**Trust level**: High. The improvement is mathematically genuine, though the full proof may not be machine-checkable.

**Example**: AlphaEvolve's new cap-set-free construction for `cap_set`, where the output array was verified by hand to contain no three-term arithmetic progressions.

---

## Tier 3 — Formal Proof

**Definition**: The construction and its correctness have been verified by a proof assistant (e.g., Lean 4, Coq, Isabelle).

**Requirements**:
- Tier 2 satisfied
- Lean/Coq/Isabelle proof file that compiles without errors
- Proof covers: (a) the construction is valid, (b) the score matches the claimed value

**Trust level**: Very high. The result is as certain as any mathematical proof can be.

**Example**: AlphaEvolve's improvement of the finite field Kakeya bound for d=3 (`number_theory/finite_field_kakeya/d3`) was accompanied by a complete Lean 4 proof — the first machine-verified improvement of a classical combinatorics bound. This is described in detail in the AlphaEvolve paper ("Mathematical Discovery at Scale", Google DeepMind, 2025).

---

## Summary Table

| Tier | Name | Human Review | Machine Proof | Trust |
|---|---|---|---|---|
| 0 | Score Improvement | ✗ | ✗ | ⚠ Low |
| 1 | Reproducible Score | ✗ | ✗ | ● Medium |
| 2 | Mathematical Verification | ✓ | ✗ | ●● High |
| 3 | Formal Proof | ✓ | ✓ (Lean/Coq) | ●●● Very High |

## Reporting Improvements

When submitting an improvement to a problem in this library, please note the verification tier in your PR or issue. For Tier 3, include the proof file path.

A typical PR description:

```
Improves geometry/kissing_number_11d from 593 to 594.
Verification tier: 1 (Reproducible).
Code: src/autoresearch_problems/problems/geometry/kissing_number_11d/initial_program.py
Reproducible across 5 runs on two machines.
```
