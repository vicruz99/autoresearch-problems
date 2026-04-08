# Kissing Number Problem — Dimension 11

## Problem

The **kissing number** C(n) is the maximum number of non-overlapping unit
spheres that can simultaneously touch a central unit sphere in n-dimensional
space.

## Formulation

By a standard lemma, a valid kissing configuration of size |C| is certified by
a set C ⊂ R^n with 0 ∉ C satisfying:

    min_{x ≠ y ∈ C} ||x - y||  ≥  max_{x ∈ C} ||x||

The unit spheres centred at { 2x/||x|| : x ∈ C } then form a valid kissing
configuration of size |C|.

## Task

Implement `solve(dimension)` returning a NumPy array of shape `(n, dimension)`
representing a set C ⊂ R^11.  The goal is to **maximise n** (the number of
points) subject to the constraint above.

You may return either integer or floating-point coordinates. Integer coordinates
are checked exactly; floats use a small tolerance.

## Known Bounds (dimension 11)

| Bound | Value |
|-------|-------|
| Best known lower bound | **593** (AlphaEvolve, 2025) |
| Previous lower bound | 592 |
| Known upper bound | 868 |

## Hints

- Lattice-based constructions (e.g. sections of the E8 or Leech lattice)
  provide strong starting points.
- Integer coordinates avoid floating-point issues in the constraint check.
- The construction that achieved 593 was found by AlphaEvolve using
  evolutionary search over heuristic programs.
