# Kissing Number Problem

## Problem Statement

Find the maximum number of non-overlapping unit spheres in **d-dimensional**
Euclidean space that can simultaneously touch a central unit sphere.

This is the **kissing number problem** — one of the classical open problems in
discrete geometry.

## Known values

| Dimension d | Kissing number K(d) |
|-------------|---------------------|
| 1           | 2                   |
| 2           | 6                   |
| 3           | 12                  |
| 4           | 24                  |
| 8           | 240                 |
| 24          | 196 560             |

For most other dimensions (including d=3 above 12), the exact value is not known.

## Your Task

Implement a function `solve()` that returns a **NumPy array of shape `(k, d)`**
where:

- Each row is the **centre** of a kissing sphere.
- Every centre must be at **distance exactly 2** from the origin (unit radius +
  unit radius = touching).
- Every pair of centres must be at **distance ≥ 2** (non-overlapping).
- Maximise `k` — the number of spheres.

The default problem instance uses `d = 3`, where the known optimum is `k = 12`.

## Constraints

- Output shape: `(k, 3)` for `d=3`
- `||centre_i||₂ = 2.0` for all `i`  (tolerance `1e-6`)
- `||centre_i - centre_j||₂ ≥ 2.0` for all `i ≠ j`  (tolerance `1e-6`)

## Hints

- In 3D the 12 kissing spheres correspond to the vertices of a regular
  icosahedron scaled to lie on the sphere of radius 2.
- Consider placing centres at `2 * v / ||v||` where `v` are the vertices
  of a suitable polytope.
