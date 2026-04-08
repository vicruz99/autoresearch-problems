# Kissing Number Problem — Dimension 5

## Problem

The **kissing number** K(n) is the maximum number of non-overlapping unit
spheres that can simultaneously touch a central unit sphere in n-dimensional
space.

This is an **open problem** in dimension 5.

## Formulation

By a standard lemma, a valid kissing configuration of size |C| is certified by
a set C ⊂ R^n with 0 ∉ C satisfying:

    min_{x ≠ y ∈ C} ||x - y||  ≥  max_{x ∈ C} ||x||

The unit spheres centred at { 2x/||x|| : x ∈ C } then form a valid kissing
configuration of size |C|.

## Task

Implement `solve(dimension)` returning a NumPy array of shape `(n, dimension)`
representing a set C ⊂ R^5.  The goal is to **maximise n** (the number of
points) subject to the constraint above.

You may return either integer or floating-point coordinates. Integer coordinates
are checked exactly; floats use a small tolerance.

## Known Bounds (dimension 5)

| Bound | Value |
|-------|-------|
| Best known lower bound | **40** (AlphaEvolve matched, 2025) |
| Known upper bound | 44 |

## Hints

- AlphaEvolve matched the lower bound of 40 but did not improve it — there
  may be room for a better construction between 40 and 44.
- The D5 root system provides a good starting point (40 minimal vectors of the
  checkerboard lattice D5).
- Integer coordinates avoid floating-point issues in the constraint check.
