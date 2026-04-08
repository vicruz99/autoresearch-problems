# Kissing Number Problem — Dimension 3

## Problem

The **kissing number** K(n) is the maximum number of non-overlapping unit
spheres that can simultaneously touch a central unit sphere in n-dimensional
space.

This is a **solved problem**: K(3) = 12 was proved in 1953.  This variant
serves as a pedagogical target and validation benchmark.

## Formulation

By a standard lemma, a valid kissing configuration of size |C| is certified by
a set C ⊂ R^n with 0 ∉ C satisfying:

    min_{x ≠ y ∈ C} ||x - y||  ≥  max_{x ∈ C} ||x||

The unit spheres centred at { 2x/||x|| : x ∈ C } then form a valid kissing
configuration of size |C|.

## Task

Implement `solve(dimension)` returning a NumPy array of shape `(n, dimension)`
representing a set C ⊂ R^3.  The goal is to **maximise n** (the number of
points) subject to the constraint above.

You may return either integer or floating-point coordinates. Integer coordinates
are checked exactly; floats use a small tolerance.

## Known Bounds (dimension 3)

| Bound | Value |
|-------|-------|
| Exact kissing number | **12** (proved 1953) |
| Known upper bound | 12 |

## Hints

- The 12 optimal points are the vertices of a regular icosahedron.
- All icosahedron vertices have the same norm, and the minimum edge length
  equals that norm — so the set-C lemma is satisfied with zero margin.
- This is a great starting point for understanding the formulation before
  tackling open problems in higher dimensions.
